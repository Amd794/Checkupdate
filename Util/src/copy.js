// ==UserScript==
// @name         Ò»¼ü¸´ÖÆ
// @namespace    http://tampermonkey.net/
// @version      0.0.1
// @description  try to take over the world!
// @author       AMD794

// @require      http://apps.bdimg.com/libs/jquery/2.1.4/jquery.min.js
// @require      https://cdnjs.cloudflare.com/ajax/libs/clipboard.js/2.0.6/clipboard.min.js

// @match        https://mail.qq.com/*
// ==/UserScript=

let clipboard = new ClipboardJS('#copy_btn', {
  target: trigger => trigger.previousElementSibling
});
const tooltip = $('#tooltip');
clipboard.on('success', e => {
  setTimeout(() => {
    e.clearSelection();
  }, 500)
  $(e.trigger).parent().css({
        "background": "#ebebeb",
        "font-size": "28px;",
      }).siblings().css({
        "background": "#fff",
        "font-size": "28px;",
      });
});