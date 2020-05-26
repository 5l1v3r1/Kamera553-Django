function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        var csrftoken = getCookie('csrftoken');
        // Setup ajax connections safetly

        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });

    function send(){
        var mail = "";
        var password = "";
        var name = "";
        var surname = "";

        if(document.getElementById("MainPassword").value != document.getElementById("RePassword").value){
            password = "Şifreniz eşleşmiyor!";
        }

        if(document.getElementById("MainPassword").value.length < 8 || document.getElementById("MainPassword").value.length > 16)
        {
            password = password + "\nŞifreniz en az 8 en fazla 16 karakterden oluşmalı";     
        }

        if(/^\S+/.test(document.getElementById("MainPassword")) == false){
            password = password + "\nŞifreniz boşluk barındıramaz!"
        }

        document.getElementById("PasswordErrorArea").innerText = password;

        if(/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(document.getElementById("MainMail").value) == false)
        {
            mail = "\nLütfen doğru düzgün mail adresini giriniz.(example@domain.com)";
        }
      
        document.getElementById("MailErrorArea").innerText =  mail;

        
        if(/^[a-zA-Z ]+$/.test(document.getElementById("MainName").value) == false){
            name = "Adınız sadece harf içerebilir.";
        }

        document.getElementById("NameErrorArea").innerText = name;

        
        if(/^[a-zA-Z ]+$/.test(document.getElementById("MainSurname").value) == false){
            surname = "Soyadınız sadece harf içerebilir.";
        }

        document.getElementById("SurnameErrorArea").innerText = surname;

        if(mail == "" && password == "" && name == "" && surname == ""){
            document.getElementById("MainName").value = document.getElementById("MainName").value.trim();
            document.getElementById("MainSurname").value = document.getElementById("MainSurname").value.trim();
            document.getElementById("MainMail").value = document.getElementById("MainMail").value.trim();
            document.getElementById("MainPassword").value = document.getElementById("MainPassword").value.trim();
            document.getElementById("RePassword").value = document.getElementById("RePassword").value.trim();
            document.getElementById("MainForm").submit();
    }
}