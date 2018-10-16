//gen-shader
//written by Tim Caldwell
// a simple example of how to use continuous parameters to perform switching functions
#ifdef GL_ES
precision mediump float;
#endif

uniform float u_time;
uniform float u_x0;
uniform float u_x1;

void main() {
    vec3 colour = vec3(0.0,0.0,0.0);
    if(u_x0 < (1.0 / 3.0)){
        colour[0] = 1.0;
        }
    else if(u_x0 > (2.0 / 3.0)){
        colour[1] = 1.0;
        }
    else{
        colour[2] = 1.0;
        }
    if(u_x1 < (1.0 / 3.0)){
        colour[1] = 1.0;
        }
    else if(u_x1 > (2.0 / 3.0)){
        colour[2] = 1.0;
        }
    else{
        colour[0] = 1.0;
        }
    gl_FragColor = vec4(colour, 1.0); 
	 
}
