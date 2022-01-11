//1-input
//written by Tim Caldwell
#ifdef GL_ES
precision mediump float;
#endif

uniform vec2 u_resolution;
uniform float u_time;
varying vec2 v_texcoord;
uniform sampler2D u_tex0;
uniform float u_x0;
uniform float u_x1;
uniform float u_x2;
uniform float u_x3;

void main() {
    vec2 pos = v_texcoord;
    vec4 tex_in = texture2D(u_tex0, pos);
    float alpha = u_x3 / 10.0;
    if(u_x3 == 1.0){alpha = 1.0;}
    vec4 color = vec4(0.0,0.0,0.0, alpha);
    vec2 pos_norm = gl_FragCoord.xy/ u_resolution.xy;

    if(pow(pos_norm.x - u_x0,2.0) + pow(pos_norm.y - u_x1,2.0) < pow(u_x2,2.0) ){
        color = vec4(tex_in[0],tex_in[1],tex_in[2], min(tex_in[3], 1.0) );
}

    gl_FragColor = color;

}
