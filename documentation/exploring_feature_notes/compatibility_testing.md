
# some of what follows is out of date since i have improved a number of problems since i did this. i will have to revisit this page with updates soon !

# compatibility testing

so far i have only been using a small selection of video files while running **r_e_c_u_r** .

i want to try it with a number of different video containers , codecs , resolutions , lengths etc on
both hdmi and composite displays. by compiling and downloading a number of test clips from various places online ,
i now have a folder of videos named in this format : 'width-container-codec'

clip | expectation | results
--- | --- | ---
120-mov-svq1.mov | i wouldnt expect/need this to play with apples custom codec | omx cant reconise codec
240-webm-vp8.webm | i believe vp8 codec is supported on omx but not sure if webm container is | omx cant play webm
360-webm-vp8.webm | same as above | ""
480-avi-mjpeg.avi | this should play fine | ~~wont map `dbus exception no reply`~~ on second try it does map but doesnt play - normal omx player opens but cant play it either
480-flv-vp6.flv | i think this should work although not too worried about supporting flv ! | omx cant play this ?
576-mov-mjpeg.mov | this should work | this works surprisingly well - never lags on load
576-mp4-h264.mp4 | this should work fine | plays good, sometimes lags on custom start
720-mkv-h264.mkv | this should play fine - interested if seeking / sublooping looks ok | plays ok , customstart seems to weirdly jump to middle ...
720-mp4-h264.mp4 | this should play fine | plays good, sometimes lags on load
720-mp4-h264-60fps | ~~my computer struggles to play this~~ think just a laggy video | plays suprisingly well - never lags on custom start
1080-avi-mpeg4.avi | i think this should play ok | does play - sometimes struggles to load the next loop though - similar to the other 1080 one but a bit better (seems to load if current video is paused)
1080-flv-flv1.flv | wouldnt expect/need flv with custom codec | omx doesnt recognize codec
1080-mkv-h264-60mbps.mkv | dont expect this to work | surprisingly this video played though on pi (didnt even open on my computer.) however is showing a weird new bug where when the video finished , the next one wont load but also wont error... _UPDATE: works now gpu has more memory_
1080-mp4-h264.mp4 | hopefully this plays okay ?? | this wouldnt load , error getting video length : `dbus exception no reply` (although it played ok in normal omxplayer) _UPDATE: works now gpu has more memory_
error-mkv-mpeg4.mkv | should fail but not sure how.. | just wont load

an interesting note : ~~all the videos above behaved the same on hdmi and composite out except for 1080-mp4-h264 which didnt have the failing to load next problem , instead , would flash green for a bit at the start of each clip even on custom starts~~ this also started happening on hdmi out - seems to be unpredictable how it handles 1080p files

## the same mp4 video at different resolutions

i use adobe premiere to edit videos. i imported a raw 10s mts file from a digital camera and exported 3 times : 480 , 720 and 1080. these three were loaded and tested on recur :

- 480 played fine - no lags when custom starting (both on hdmi and composite)
- 720 played ok - video played through and loaded all good. sometimes would lag on custom start point , seemed to be better / not do this when composite out mode
- ~~1080 doesnt work - the video can play through once alright , but it seems like the omxplayer/dbus connection cant load another 1080 file while an existing 1080 file is playing~~

UPDATE: turns out the 1080 files couldnt load because the pi hadnt been assigned enough memory to its gpu . i added `gpu_mem=448` to the config.txt and now 1080 videos seem to load and loop just fine. (still sometimes lags when change is triggered/ custom start)

# summary of findings :

- .mp4 containers with h.264 codec seems to be the best format - long videos play fine (tested up to 3 hours) besides some display confusion for durations over 99 minutes as expected. can play files up to 1080 resolution fine. the chances of micro lags on changeover/custom starts seems to increase with higher resolution (no problems with 480 now) but can still be avoided by setting another custom start just after the position that is lagging.
- .avi , .mov and .mkv containers also work. h.264 is best , mjpeg worked in a .mov container but not in .avi ... there was some issues with setting custom start in one of the .mkv files i tried - this might need some more investigation...
