//pro-shader
//written by Tim Caldwell
#ifdef GL_ES
precision highp float;
#endif

varying vec2 v_texcoord;
uniform sampler2D u_tex0;
uniform vec2 u_resolution;
uniform float u_time;
uniform float u_x0;
uniform float u_x1;
uniform float u_x2;

void main(){

vec2 pos = v_texcoord * u_resolution;
vec2 centre = u_resolution / 2.0;
vec2 norm = pos - centre;
//float r = distance(u_resolution, pos);
float r = length(norm);
//float theta = acos(norm.x / r);
float theta = atan(pos.y / pos.x);
//float newTheta = theta + 0.000;
theta += u_time*u_x0;
//pos.x = r*cos(theta) + centre.x;
pos.y = 4.0*u_x1*r*sin(theta) + centre.y;
pos.x = 4.0*(1.0-u_x2)*r*cos(theta) + centre.x;
//pos.y = r*sin(radians(theta)) + centre.y;




vec4 color = texture2D(u_tex0, pos / u_resolution);

gl_FragColor = color;


}



