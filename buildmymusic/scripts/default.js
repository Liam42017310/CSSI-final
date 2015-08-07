$(document).ready(function()
  {
     var watermark = 'Search an artist, song, or album here';
     $('#searchbar').blur(function(){
      if ($(this).val().length == 0)
        $(this).val(watermark).addClass('watermark');
     }).focus(function(){
      if ($(this).val() == watermark)
        $(this).val('').removeClass('watermark');
     }).val(watermark).addClass('watermark');
  }
);
