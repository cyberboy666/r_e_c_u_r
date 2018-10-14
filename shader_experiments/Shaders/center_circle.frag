precision mediump float;
uniform float u_time;
uniform vec2 u_resolution;

void main(void) {

    vec2 center = u_resolution / 2.0;
    vec2 pos = gl_FragCoord.xy;
    vec2 dist = center - pos;
    float len = length(dist);

    vec3 color = vec3(0.0, 0.0, 0.0);

    if (len < 5.0){ color.r = 1.0; }

	gl_FragColor = vec4(color, 1.0);
}
