# compatibility testing

so far i have only been using a small selection of video files while running **r_e_c_u_r** .

i want to try it with a number of different video containers , codecs , resolutions , lengths etc on
both hdmi and composite displays. by compiling and downloading a number of test clips from various places online ,
i now have a folder of videos named in this format : 'width-container-codec'

clip | expectation | results
--- | --- | ---
120-mov-svq1.mov | i wouldnt expect/need this to play with apples custom codec |
240-webm-vp8 | i believe vp8 codec is supported on omx but not sure if webm container is |
360-webm-vp8.webm | same as above |
480-avi-mjpeg.avi | this should play fine
480-flv-vp6.flv | i think this should work although not too worried about supporting flv ! |
576-mov-mjpeg.mov | this should work |
576-mp4-h264.mp4 | this should work fine |
720-mkv-h264.mkv | this should play fine - interested if seeking / sublooping looks ok |
720-mp4-h264.mp4 | this should play fine |
720-mp4-h264-60fps | my computer struggles to play this |
1080-avi-mpeg4.avi | i think this should play ok |
1080-flv-flv1.flv | wouldnt expect/need flv with custom codec |
1080-mkv-h264-60mbps.mkv | dont expect this to work |
1080-mp4-h264.mp4 | hopefully this plays okay ?? |
error-mkv-mpeg4.mkv | should fail but not sure how.. |
