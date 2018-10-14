//gen-shader
#ifdef GL_ES
precision mediump float;
#endif

uniform vec2 u_resolution;
uniform float u_time;
uniform float u_x0;

void main() {
    vec2 pos = gl_FragCoord.xy;
    vec2 st = gl_FragCoord.xy/u_resolution.xy;
    st.x *= u_resolution.x/u_resolution.y;

    vec3 color = vec3(0.0,0.0,0.0);

    color += vec3(sin(0.05*pos.x - cos(u_x0*u_time)) + cos(0.05*pos.x/(0.1 + abs(cos(u_time/5.0)))),0.0,0.0);
    color += vec3(sin(0.05*pos.y - cos(u_time/5.0)) + cos(0.05*pos.y/(0.1 + abs(cos(u_time/5.0)))),0.0,0.0);
    color += vec3(0.0, 0.0, sin(u_time));

    gl_FragColor = vec4(color,1.);

}
