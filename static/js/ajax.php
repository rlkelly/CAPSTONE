    <?php
    // set feed URL
    $feedURL  = 'http://gdata.youtube.com/feeds/api/standardfeeds/most_viewed';
    $feedURL1 = 'http://gdata.youtube.com/feeds/api/videos/-/Travel/';
    $feedURL2 = 'http://gdata.youtube.com/feeds/api/videos/-/Comedy/';
    $feedURL3 = 'http://gdata.youtube.com/feeds/api/videos/-/Film/';
    $feedURL4 = 'http://gdata.youtube.com/feeds/api/videos/-/animation/';
    $feedURL5 = 'http://gdata.youtube.com/feeds/api/videos/-/lifestyle/';
    
    $pg = $_REQUEST['p'];
    
	$i = 0;
    $rssfeed = $feedURL2;
    
    // read feed into SimpleXML object
    $sxml = simplexml_load_file($rssfeed);
    ?>
      <h1><?php echo $sxml->title; ?></h1>
    <?php
    // iterate over entries in feed
    foreach ($sxml->entry as $entry) {
      // get nodes in media: namespace for media information
      $media = $entry->children('http://search.yahoo.com/mrss/');
      
      // get video player URL
      $attrs = $media->group->player->attributes();
      $watch = $attrs['url']; 
      
      // get video thumbnail
      $attrs = $media->group->thumbnail[0]->attributes();
      $thumbnail = $attrs['url']; 
            
      // get <yt:duration> node for video length
      $yt = $media->children('http://gdata.youtube.com/schemas/2007');
      $attrs = $yt->duration->attributes();
      $length = $attrs['seconds']; 
      
      // get <yt:stats> node for viewer statistics
      $yt = $entry->children('http://gdata.youtube.com/schemas/2007');
      $attrs = $yt->statistics->attributes();
      $viewCount = $attrs['viewCount']; 
      
      // get <gd:rating> node for video ratings
      $gd = $entry->children('http://schemas.google.com/g/2005'); 
      if ($gd->rating) {
        $attrs = $gd->rating->attributes();
        $rating = $attrs['average']; 
      } else {
        $rating = 0; 
      } 
      ?>
      <div class="box">
        <h3><a href="<?php echo $watch; ?>" target="_blank"><?php echo $media->group->title; ?></a></h3>
        <p>
          <span class="thumbnail">
            <a href="<?php echo $watch; ?>" target="_blank"><img src="<?php echo $thumbnail;?>"></a>
          </span> <br>
          <span class="attr">By:</span> <?php echo $entry->author->name; ?> - 
          <span class="attr">Duration:</span> <?php printf('%0.2f', $length/60); ?> 
          min. <br>
          <span class="attr">Views:</span> <?php echo $viewCount; ?> - 
          <span class="attr">Rating:</span> <?php echo $rating; ?> 
        </p>
      </div>      
    <?php 
	    if (++$i >= 2) {
    	  break;
  		}
	} // end foreach
	
	?>
    
    <div class="infinitescroll"></div>