console.log("loaded web_widget.js");
window.__bot.host_parent = window.location.origin;
console.log(window.__bot.host_parent);
// appending iframe div start
if (window.location.origin == "file://" || window.location.origin == "null") {
    chatbot_div_width = "473px";
    chatbot_div_height = "616px";
} else {
    chatbot_div_width = "270px";
    chatbot_div_height = "310px";
}
let div_iframe = document.createElement("div");
div_iframe.id = "chatbot-chat";
div_iframe.style =
    "position:relative; background-color:transparent; border:none;"
    
div_iframe.innerHTML =
    "" +
    '   <iframe src="' +
    window.__bot.host_webbot +
    "/chat.html?web_uid=" +
    window.__bot.web_uid +
    "&host_parent=" +
    window.__bot.host_parent +
    "&host_backend=" +
    window.__bot.host_backend +
    "&website_user=" +
    window.__bot.website_user +
    "&bot_name=" +
    window.__bot.bot_name +
    '" id="chatbot-chat-frame" style="pointer-events: all; background: none; border: 0px; float: none; position: fixed; z-index:999; right: 0px; bottom: 0px; width: 270px; height: 310px; margin: 0px; padding: 0px; min-height: 0px;">' +
    "   </iframe>";
document.body.appendChild(div_iframe);
// appending iframe div end

var chatbot_div = document.getElementById("chatbot-chat");
window.onmessage = function (e) {
    console.log(e);
    if (e.data == "minimized") {
        // chatbot_div.style.width = "270px";
        // chatbot_div.style.height = "310px";
        console.log("maximized");
        document.getElementById("chatbot-chat-frame").style.width = "270px";
        document.getElementById("chatbot-chat-frame").style.height = "310px";
    } else if (e.data == "maximized") {
        // chatbot_div.style.width = "473px";
        // chatbot_div.style.height = "616px";
        document.getElementById("chatbot-chat-frame").style.width = "403px";
        document.getElementById("chatbot-chat-frame").style.height = "600px";
    }
};

