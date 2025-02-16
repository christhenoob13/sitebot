io.emit('join', Room)

io.on('sendMessage', (msg) => {
  const reply = sendReply(msg?.reply)
  if (reply?.error){
    sendMessage({
      data: reply.error,
      id: msg.id
    })
  }else{
    sendMessage({
      data: msg.data,
      reply_to: reply,
      id: msg.id
    })
  }
})

io.on('unsendMessage', (data) => {
  unsendMessage(data.id)
})


// when user enter a message
function execute(){
  const input = $('#input');
  const value = input.val().trim();
  let data = null;
  if ($('.REPLY').is(':visible')) data = getReplyData();
  if (value){
    const $ID = messageID(20)
    sendMessage({
      data: value,
      reply_to: data ? {
        id: data?.id,
        text: data?.text,
        image: data?.images,
        video: data?.video,
        sender: data?.sender
      }:null,
      id: $ID
    }, true)
    input.val('');
    io.emit('recieveMessage', {
      text: value,
      reply_to: data ?? '',
      id: $ID,
      room: Room
    });
  }
}