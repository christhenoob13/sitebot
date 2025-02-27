// Auto scroll to the bottom message
function scroll(){
  window.scrollTo({
    top: document.body.scrollHeight,
    behavior: 'smooth'
  })
  const msg = document.getElementById('msg-cont');
  msg.scrollTop = msg.scrollHeight;
}

// Get the reply data
const getReplyData = () => {
  const sender = $('.REPLY .data-user').text()
  const messageID = $('.REPLY .data-message_id').text()
  const text = $('.REPLY .data-text').text()
  let buttons = $('.REPLY .data-buttons').text()
  let images = $('.REPLY .data-images').text()
  let videos = $('.REPLY .data-videos').text()
  console.log(buttons);
  if (images) images = images.split(',');
  if (videos) videos = videos.split(',');
  $('.REPLY').remove()
  return {
    id: messageID,
    text: text,
    sender: sender,
    images: images || [],
    videos: videos || []
  }
}

// Message with buttons
const buttons = (button, body) => {
  button.forEach(btn => {
    const btn_link = $('<a>').addClass('btn-a');
    const btn_click = $('<button>');
    if (btn?.a){
      for (let key in btn.a){
        if (btn.a.hasOwnProperty(key)){
          btn_link.attr(key, btn.a[key])
        }
      }
    }
    if (btn?.style){
      btn_click.css(btn.style)
    }
    btn_click.text(btn?.text ?? "Click")
    body.append(btn_link.append(btn_click))
  })
}

// random message id
const messageID = (count) => {
  const char = "abcdefghijklmnopqrstuvwxyz1237654098QWERTYUIOPASDFGHJKLZXCVBNM";
  let id = 'MSG-'
  for (let i=0;i<count*2;i++){
    const index = Math.floor(Math.random() * char.length)
    id += char[index-1]
  }
  return id
}

// check if link or path
const attachCheck = (src) => {
  if (src.includes('https://')){
    return src
  }else{
    return basePath + src
  }
}

// Create an attachemnt imagee
const createImage = (attachment) => {
  const image = $('<img />', {
    src: attachCheck(attachment.src),
    alt: attachment?.title ?? 'No title!',
    height: attachment?.height ?? null
  })
  return image
}

// Create video
const createVideo = (video) => {
  return $("<video>")
    .attr('height', video?.height ?? null)
    .attr('controls', '')
    .append($("<source />").attr('src', attachCheck(video.src)))
}

// Format the text
const MATCHER = (reg,text, func) => {
  let inp = text.match(reg)
  if (inp){
    func(inp)
  }
}
const text = (text, $body) => {
  const span = (t) => `${t==='>'?'&gt':'&lt'}`;
  text = text.replace(/</g, span('<')).replace(/>/g, span('>'));
  text = text.replace(/\n/g, '<br>')

  //text = text.replace(/:line:/g, '<hr>')
  
  const linkRegex = /!\[([^\]]+)\]\(([^\)]+)\)/g
  const iconRegex = /:icon\[(.*?)\]/g
  
  // link
  MATCHER(linkRegex, text, (links) => {
    for (const link of links){
      let [_XA,_XB] = link.split("](");
      text = text.replace(link, `<a target="_blank" href="${_XB.slice(0,_XB.length-1)}">${_XA.slice(2)}</a>`);
    }
  })
  // icon
  MATCHER(iconRegex, text, (icons) => {
    for (const icon of icons){
      text = text.replace(icon, `<i class="${icon.split(':icon[')[1].slice(0,icon.split(':icon[')[1].length-1)}"></i>`)
    }
  })
  // bold text
  MATCHER(/:bold\[(.*?)\]/g, text, (bolds) => {
    for (const bold of bolds){
      text = text.replace(bold, `<b>${bold.split(":bold[")[1].slice(0, bold.split(':bold[')[1].length-1)}</b>`)
    }
  })
  // text Color
  MATCHER(/:[a-zA-Z0-9\-]+\[(.*?)\]/g, text, ($COLORS)=>{
    for (const color of $COLORS){
      const $ind = color.indexOf('[');
      const $color = color.slice(1,$ind)
      const $text = color.slice($ind+1, color.length-1)
      switch ($color){
        case 'danger-color':
          text = text.replace(color, `<span style="color:#d9534f">${$text}</span>`)
        case 'warning-color':
          text = text.replace(color, `<span style="color:#f0ad4e">${$text}</span>`)
        case 'info-color':
          text = text.replace(color, `<span style="color:#5bc0de">${$text}</span>`)
        case 'success-color':
          text = text.replace(color, `<span style="color:#5cb85c">${$text}</span>`)
        case 'primary-color':
          text = text.replace(color, `<span style="color:#0275d8">${$text}</span>`)
      }
    }
  })
  $body.append($('<p>').html(text));
}

// Reply method
$('#rply-remove').click(function(){$('.REPLY').remove()})
const removeMe = (cls) => {
  $(cls).hide()
  $(cls).html('')
}
function PorEacg(){
  // View Image
  $('.attachment img').click(function(){
    const me = $(this)[0]
    Swal.fire({
      text: me.alt,
      imageUrl: me.src,
      imageAlt: me.alt,
      showConfirmButton: false
    })
  })
  // handle reply
  $('.message').each(function(_,message){
    //console.log(message)
    $(message).dblclick(()=>{
      showOtherClicks(message)
    })
  })
}

function showOtherClicks(data){
  const user = $(data).find('.label').attr('data-text')
  const messageID = $(data).parent().attr('id')
  let body = $(data).find('.body > p').html().replace(/<br>/g, '\n')
  let buttons = [];
  let images = [];
  let videos = [];
  $(data).find('a.btn-a').each(function(){
    buttons.push({
      href: $(this).attr('href'),
      text: $(this).text()
    })
  })
  $(data).find('img').each(function(){
    images.push($(this).attr('src'))
  })
  $(data).find('video > source').each(function(){
    videos.push($(this).attr('src'))
  })
  $('.REPLY').remove()
  const reply = $('<div>').addClass('REPLY')
  reply.html(`
    <div style="display:none">
      <p class="data-message_id">${messageID}</p>
      <p class="data-user">${user}</p>
      <p class="data-text">${body}</p>
      <p class="data-buttons">${JSON.stringify(buttons)}</p>
      <p class="data-images">${images}</p>
      <p class="data-videos">${videos}</p>
    </div>
    <div class="rply-text">
      <p>Reply to ${user==='You'?'your':user+'\'s'} message</p>
    </div>
    <div class="rply-remove">
      <button id="rply-remove" onclick="removeMe('.REPLY')"><i class="fa-solid fa-remove"></i></button>
    </div>
  `)
  $('.input_container').prepend(reply)
}