//0-input
//written by Ben Caldwell
#ifdef GL_ES
precision mediump float;
#endif

uniform vec2 u_resolution;
uniform float u_time;
uniform float u_x0;
uniform float u_x1;
uniform float u_x2;
uniform float u_x3;

void main() {

    vec3 color = vec3(0.0,0.0,0.0);
    vec2 pos = gl_FragCoord.xy;
    vec2 st = gl_FragCoord.xy/u_resolution.xy;
    st.x *= u_resolution.x/u_resolution.y;

    color += vec3(u_x0*sign(sin(0.05*pos.x - u_time + sin(0.05*pow(pos.y,(0.7 + u_x1)) - u_time))),0.,0.);
    color += vec3(0., 0., sign(cos(0.05*pos.x*u_x2 - 2.0*u_time + 5.0*u_x3*sin(0.05*pos.y - 2.0*u_time))));

    gl_FragColor = vec4(color,1.);

}
