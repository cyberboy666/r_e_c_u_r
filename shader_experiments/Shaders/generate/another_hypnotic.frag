
#ifdef GL_ES
precision mediump float;
#endif

uniform vec2 u_resolution;
uniform vec2 u_mouse;
uniform float u_time;

void main() {
    vec3 color = vec3(0.0,0.0,0.0);

    vec2 pos = gl_FragCoord.xy;
    vec2 st = gl_FragCoord.xy/u_resolution.xy;
    st.x *= u_resolution.x/u_resolution.y;

    vec2 s1 = vec2(u_resolution.x*(0.5 + 0.25*cos(u_time)), u_resolution*(0.5 + 0.25*sin(u_time)));
    vec2 s2 = vec2(u_resolution.x*(0.5 + 0.25*sin(u_time)), u_resolution*(0.5 + 0.25*cos(u_time)));
    vec2 s3 = vec2(u_resolution.x*0.5, u_resolution*0.5);
    
    float r1 = pow(pow(pos.x-s1.x,2.0) + pow(pos.y-s1.y,2.0), 0.5);
    float r2 = pow(pow(pos.x-s2.x,2.0) + pow(pos.y-s2.y,2.0), 0.5);
    float r3 = pow(pow(pos.x-s3.x,2.0) + pow(pos.y-s3.y,2.0), 0.5);
    
    color += vec3(0.5 + 0.5*sign(sin((0.1 + 0.05*sin(u_time+2.0))*r1 - 1.0*u_time)), 0.0, 0.0);
    color += vec3(0.0, 0.0, 0.5 + 0.5*sign(sin((0.1 + 0.05*sin(u_time))*r2 - 1.2*u_time)));
    color += vec3(0.0, 0.5 + 0.5*sign(sin((0.1 + 0.05*sin(u_time+0.5))*r3 - 1.1*u_time)), 0.0);



    gl_FragColor = vec4(color,1.);
}
