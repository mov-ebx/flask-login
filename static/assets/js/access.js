let switchCtn=document.querySelector("#switch-cnt"),switchC1=document.querySelector("#switch-c1"),switchC2=document.querySelector("#switch-c2"),switchCircle=document.querySelectorAll(".switch__circle"),switchBtn=document.querySelectorAll(".switch-btn"),aContainer=document.querySelector("#a-container"),bContainer=document.querySelector("#b-container"),allButtons=document.querySelectorAll(".submit"),getButtons=t=>t.preventDefault(),changeForm=t=>{switchCtn.classList.add("is-gx"),setTimeout((function(){switchCtn.classList.remove("is-gx")}),1500),switchCtn.classList.toggle("is-txr"),switchCircle[0].classList.toggle("is-txr"),switchCircle[1].classList.toggle("is-txr"),switchC1.classList.toggle("is-hidden"),switchC2.classList.toggle("is-hidden"),aContainer.classList.toggle("is-txl"),bContainer.classList.toggle("is-txl"),bContainer.classList.toggle("is-z200")},mainF=t=>{for(var e=0;e<allButtons.length;e++)allButtons[e].addEventListener("click",getButtons);for(e=0;e<switchBtn.length;e++)switchBtn[e].addEventListener("click",changeForm)};window.addEventListener("load",mainF);function signIn(n,t){document.getElementById("signin-error").style.display="none";const e={username:n,password:"_|"+t+"|0"};fetch("/api/account/signin",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(e)}).then((n=>new function(){200==n.status?window.location.reload():n.text().then((n=>new function(){document.getElementById("signin-error").innerHTML=n,document.getElementById("signin-error").style.display="block"}))}))}function signUp(e,t,n,x){if(document.getElementById("signup-error").style.display="none",t!==n)return document.getElementById("signup-error").innerHTML="Please make sure you wrote the same password twice!",void(document.getElementById("signup-error").style.display="block");const o={username:e,password:"_|"+t+"|0",email:x};fetch("/api/account/signup",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(o)}).then((e=>new function(){201==e.status?window.location.reload():e.text().then((e=>new function(){document.getElementById("signup-error").innerHTML=e,document.getElementById("signup-error").style.display="block"}))}))}function verify(e){const n={code:Number(e)};fetch("/api/account/emailverify",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(n)}).then((e=>new function(){document.getElementById("error").style.display="none",200==e.status?window.location.reload():(document.getElementById("error").style.display="block",document.getElementById("error").innerHTML="Wrong code!")})).catch((e=>console.error(e)))}function resend(){fetch("/api/account/resendverify",{method:"POST",headers:{"Content-Type":"application/json"}}).then((e=>new function(){alert("Verification code resent!")})).catch((e=>console.error(e)))}