//pro-shader
//written by Tim Caldwell
#ifdef GL_ES
precision mediump float;
#endif

varying vec2 v_texcoord;
uniform sampler2D u_tex0;
uniform vec2 u_resolution;
uniform float u_time;
uniform float u_x0;
uniform float u_x1;
uniform float u_x2;
uniform float u_x3;


void main(){

vec2 pos = v_texcoord;
//float amp =  pos.y * 0.03 + .001;
pos.x += 0.07*u_x2*sin( pos.y* 70.0*u_x3 + u_time *  1.0 );
pos.y += 0.07*u_x0*sin( pos.x* 70.0*u_x1 + u_time *  1.0);
pos.y = mod(pos.y,1.0);
pos.x = mod(pos.x,1.0);
//if(pos.y > 1.0 || pos.y < 0.0){pos.y = 0.0;}

vec4 color = texture2D(u_tex0, pos);

gl_FragColor = color;


}



