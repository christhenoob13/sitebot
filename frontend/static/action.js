function sendMessage({ id, data, reply_to, sender }, isMe=false){
  let isGlobal = false
  let isUser = false
  if (!data) return;
  if (Room==='global') isGlobal = true;
  if (sender===u_name) isUser = true;
  const youbot = () => {
    if (isGlobal && isUser) {return 'You'}
    else if (isGlobal && !isUser) {return sender}
    else if (!isGlobal && isMe) {return 'You'}
    else{ return 'BOT' }
  }
  const $message_box = $("<div>")
    .addClass(`message_box ${isMe && isUser ? 'me':'other'}`)
    .attr('id', id);
  const $message = $('<div>').addClass('message');
  const $label = $('<div>')
    .addClass('label')
    .attr('data-text', youbot())
    .text(youbot());
  const $mainMessage = $('<div>').addClass('main-message');
  
  const $body = $('<div>').addClass('body');
  const $attachment = $('<div>').addClass('attachment').hide();
  const $skeleton = $('<div>').addClass('skeleton').append($('<div>').addClass('skeleton-image'));
  
  // When the message replied to other message
  console.log(reply_to)
  if (reply_to) $label.text(`${youbot()} replied to ${reply_to?.sender===u_name?'your':reply_to.sender} message`);
  else{
    // (!) naguluhan ako dito
    const $nth = '.message_box:nth-last-child(1)';
    if ($($nth).hasClass(isUser?'me':'other')){
      const $last_sender = $(`${$nth} .label`).attr('data-text');
      if (!isUser && ($last_sender !== sender)){
        {}
      }else{
        $($nth).css('margin-bottom', '3px')
        $($label).hide()
      }
    }
  }
  
  let hasBody = false;
  let hasAttach = false;
  if (typeof data === 'string'){text(data, $body);hasBody=true}
  else {
    const { body, attachment, button } = data;
    
    body || button ? hasBody=true:hasBody;
    
    // format message
    body ? text(body, $body):null
    button ? buttons(button, $body):null
    
    // send with attachment
    if (attachment) attachment.length >= 1 ? hasAttach=true:hasAttach;
    if (attachment){
      for (const attach of attachment){
        if (attach?.type === 'image'){
          const img = createImage(attach);
          img.attr('width', '49%')
          if ((attachment.indexOf(attach)%2)!==0) img.css('margin-left', '2%')
          if (attachment.length === 1) img.css('width','100%');
          img.on('load', () => {
            $skeleton.hide();
            $attachment.show()
          })
          $attachment.append(img)
        }else if(attach?.type === 'video'){
          const video = createVideo(attach);
          video.css('width', '100%')
          video.css('border-radius', '11px')
          video[0].onloadedmetadata = function(){
            $skeleton.hide();
            $attachment.show()
          }
          $attachment.append(video)
        }else{
          $skeleton.hide()
          $attachment.show()
          $attachment.append(
            $('<div>').addClass('invalidType').append(
              $('<div>')
              .addClass('text')
              .text('Invalid attachment type')
            )
          )
        }
      }
    }
  }
  
  if (hasBody) $mainMessage.append($body);
  if (hasAttach) $mainMessage.append($skeleton).append($attachment);
  $message.append($label).append($('<div>').addClass('__message').append($mainMessage));
  $message_box.append($message);
  $('.messages').append($message_box)
  $('.other .main-message').css('border-color', isDarkmode?'var(--semiDark)':'#c5c5c4');
  $('.other .body p').css('color', isDarkmode?'var(--text)':'#1f1f1d')
  PorEacg()
  scroll()
}

function sendReply(id){
  if (!id) return null;
  if ($(`#${id}`).length === 0) {
    return {
      error: `⚠️ Message ID not found. Can't reply to the message`
    }
  }
  const data = $(`#${id} > .message`)
  const $user = $(data).find('.label').text()
  const $messageID = $(data).parent().attr('id')
  let $body = $(data).find('.body > p').html().replace(/<br>/g, '\n')
  let $images = [];
  let $videos = []
  $(data).find('img').each(function(){
    $images.push($(this).attr('src'))
  })
  $(data).find('video > source').each(function(){
    $videos.push($(this).attr('src'))
  })
  return {
    id: $messageID,
    text: $body,
    sender: $user,
    image: $images,
    video: $videos
  }
}

function unsendMessage(id){
  $(`#${id}`).remove()
}