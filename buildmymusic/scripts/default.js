
$(document).ready(function(){

  $(".like").click(function () {
    console.log(this.parentNode.parentNode.id);
    var song_title_selector = "#" + this.parentNode.id + " .song";
    var artist_name_selector = "#" + this.parentNode.id + " .artist";
    var album_name_selector = "#" + this.parentNode.id + " .album";
    var current_song = $(song_title_selector).text();
    var current_artist = $(artist_name_selector).text();
    var current_album = $(album_name_selector).text();
    var current_like = {'title': current_song, 'artist': current_artist, 'album': current_album}
    $.post("like", {'like': JSON.stringify(current_like)});
  });

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






});
