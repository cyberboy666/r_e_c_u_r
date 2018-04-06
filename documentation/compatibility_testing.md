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
480-avi-mjpeg.avi | this should play fine | wont map `dbus exception no reply`
480-flv-vp6.flv | i think this should work although not too worried about supporting flv ! | omx cant play this ?
576-mov-mjpeg.mov | this should work | this works surprisingly well - never lags on load
576-mp4-h264.mp4 | this should work fine | plays good, sometimes lags on custom start
720-mkv-h264.mkv | this should play fine - interested if seeking / sublooping looks ok | plays ok , customstart seems to weirdly jump to middle ...
720-mp4-h264.mp4 | this should play fine | plays good, sometimes lags on load
720-mp4-h264-60fps | ~~my computer struggles to play this~~ think just a laggy video | plays suprisingly well - never lags on custom start
1080-avi-mpeg4.avi | i think this should play ok | does play - sometimes struggles to load the next loop though - similar to the other 1080 one but a bit better (seems to load if current video is paused)
1080-flv-flv1.flv | wouldnt expect/need flv with custom codec | omx doesnt reconise codec
1080-mkv-h264-60mbps.mkv | dont expect this to work | suprizingly this video played though on pi (didnt even open on my computer.) however is showing a weird new bug where when the video finished , the next one wont load but also wont error...
1080-mp4-h264.mp4 | hopefully this plays okay ?? | this wouldnt load , error getting video length : `dbus exception no reply` (although it played ok in normal omxplayer)
error-mkv-mpeg4.mkv | should fail but not sure how.. | just wont load

an interesting note : all the videos above behaved the same on hdmi and composite out except for 1080-mp4-h264 which didnt have the failing to load next problem , instead , would flash green for a bit at the start of each clip even on custom starts
