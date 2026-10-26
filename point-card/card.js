(function(){
  var card=document.getElementById('card'), stage=document.getElementById('stage'),
      hint=document.getElementById('hint'), root=document.documentElement.style;
  var MAX=14;

  // how the page was opened: NFC tap vs QR/link
  try{
    var src=new URLSearchParams(location.search).get('src');
    if(src==='nfc') document.getElementById('greet').textContent='Tapped. Nice to meet you';
  }catch(e){}

  function set(px,py){            // px,py in 0..1
    root.setProperty('--mx',(px*100).toFixed(1)+'%');
    root.setProperty('--my',(py*100).toFixed(1)+'%');
    root.setProperty("--ang",((px*220+py*140)).toFixed(0)+"deg");
    root.setProperty('--ry',((px-.5)*2*MAX).toFixed(2)+'deg');
    root.setProperty('--rx',((.5-py)*2*MAX).toFixed(2)+'deg');
    root.setProperty('--glare',Math.min(1,Math.hypot(px-.5,py-.5)*2.2+.25).toFixed(2));
  }
  function stopIdle(){card.classList.remove('idle');hint.style.opacity=0}
  function reset(){set(.5,.5);root.setProperty('--glare',0)}
  reset();

  // pointer (mouse + touch drag)
  var active=false;
  function pt(e){var r=card.getBoundingClientRect();
    return [Math.min(1,Math.max(0,(e.clientX-r.left)/r.width)),Math.min(1,Math.max(0,(e.clientY-r.top)/r.height))]}
  stage.addEventListener('pointerdown',function(e){active=true;stopIdle();var p=pt(e);set(p[0],p[1])});
  stage.addEventListener('pointermove',function(e){if(active||e.pointerType==='mouse'){stopIdle();var p=pt(e);set(p[0],p[1])}});
  window.addEventListener('pointerup',function(){active=false;if(!gyro)reset()});
  stage.addEventListener('pointerleave',function(e){if(e.pointerType==='mouse'&&!gyro)reset()});

  // gyroscope (Android works directly; iOS needs a permission tap)
  var gyro=false;
  var front=document.getElementById('front'),back=document.getElementById('back'),flip=document.getElementById('flip'),flipped=false,moved=0;
  stage.addEventListener('pointerdown',function(e){moved=0;stage._x=e.clientX;stage._y=e.clientY});
  stage.addEventListener('pointerup',function(e){if(Math.hypot(e.clientX-stage._x,e.clientY-stage._y)<8)doFlip()});
  function doFlip(){
    flip.style.transition='transform .18s ease-in';flip.style.transform='rotateY(90deg)';
    setTimeout(function(){flipped=!flipped;front.hidden=flipped;back.hidden=!flipped;
      flip.style.transition='transform .18s ease-out';flip.style.transform='rotateY(0deg)'},180);
  }
  function onOrient(e){
    if(e.gamma==null||e.beta==null)return;
    gyro=true;stopIdle();
    var gx=Math.max(-30,Math.min(30,e.gamma))/60+.5,
        gy=Math.max(-30,Math.min(30,e.beta-40))/60+.5;
    set(gx,gy);
  }
  function enableGyro(){
    window.addEventListener('deviceorientation',onOrient,true);
  }
  var D=window.DeviceOrientationEvent;
  if(D&&typeof D.requestPermission==='function'){
    // iOS: ask on the first touch of the card, as required
    document.addEventListener('click',function once(){
      document.removeEventListener('click',once);
      D.requestPermission().then(function(s){if(s==='granted')enableGyro()}).catch(function(){});
    });
    hint.textContent='Tap anywhere to enable tilt';
  }else if(D){enableGyro()}
})();
