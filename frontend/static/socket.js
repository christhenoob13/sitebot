io.emit('join', Room)

io.on('sendMessage', (msg) => {
  if (msg?.isUser){
    sendMessage(msg, true)
  }else{
    const reply = sendReply(msg?.reply)
    if (reply?.error){
      sendMessage({
        data: reply.error,
        id: msg.id,
        sender: 'BOT'
      })
    }else{
      sendMessage({
        data: msg.data,
        reply_to: reply,
        id: msg.id,
        sender: "BOT"
      })
    }
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
    io.emit('sendMessage', {
      data: value,
      id: $ID,
      sender: u_name,
      reply_to: data?{
        id: data?.id,
        sender: data?.sender
      }:null,
      room: Room,
      isUser: true
    })
    
    input.val('');
    
    io.emit('recieveMessage', {
      text: value,
      reply_to: data ?? '',
      id: $ID,
      room: Room,
      sender: u_name ?? 'Sitebot user' // chat.html (ln:32)
    })
  }
}