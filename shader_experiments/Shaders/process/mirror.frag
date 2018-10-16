//pro-shader
//written by Tim Caldwell
//this is a basic example of how to effect input textures position
#ifdef GL_ES
precision mediump float;
#endif

varying vec2 v_texcoord;
uniform sampler2D u_tex0;
uniform vec2 u_resolution;
uniform float u_time;
uniform float u_x0;
uniform float u_x1;

void main(){

vec2 pos = v_texcoord;

if(pos.x > u_x0){pos.x = 1.0 - pos.x;}
if(pos.y < u_x1){pos.y = 1.0 - pos.y;}
vec4 color = texture2D(u_tex0, pos);

gl_FragColor = color;


}



