
varying vec2 tcoord;       //
uniform sampler2D tex;     // texture one
uniform sampler2D tex2;    // texture two
uniform vec2 tres;         // size of texture (screen)
uniform vec4 fparams;      // 4 floats coming in
uniform ivec4 iparams;     // 4 ints coming in
uniform float ftime;       // 0.0 to 1.0
uniform int itime;         // increases when ftime hits 1.0
//f0:key luma:
//f1:key range:
//f2:edge opacity:

   float f0 = mix(0.0, 1.0, fparams[0]);
   float f1 = mix(0.0, 0.5, fparams[1]);
   float f2 = mix(0.0, 1.0, fparams[2]);

//---------------------------------------------------------------------------------------------------

vec3 rgb2hsv(vec3 c)
{
    vec4 K = vec4(0.0, -1.0 / 3.0, 2.0 / 3.0, -1.0);
    vec4 p = mix(vec4(c.bg, K.wz), vec4(c.gb, K.xy), step(c.b, c.g));
    vec4 q = mix(vec4(p.xyw, c.r), vec4(c.r, p.yzx), step(p.x, c.r));

    float d = q.x - min(q.w, q.y);
    float e = 1.0e-10;
    return vec3(abs(q.z + (q.w - q.y) / (6.0 * d + e)), d / (q.x + e), q.x);
}

vec3 hsv2rgb(vec3 c)
{
    vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
    vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
    return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
}



void main() {

   vec3 outc;
   vec4 base  = texture2D(tex, tcoord.xy);
   vec4 blend = texture2D(tex2, tcoord.xy);

   vec3 hsv = rgb2hsv(base.rgb);

   if( (hsv.z > (f0-f1)) && (hsv.z < (f0+f1)) ){
      if(hsv.z-(f0-f1) < f2){
         outc = mix(base.rgb,blend.rgb,(hsv.z-(f0-f1))/f2);
      } else if((f0+f1)-hsv.z < f2){
         outc = mix(base.rgb,blend.rgb,((f0+f1)-hsv.z)/f2);
      } else {
         outc = blend.rgb;
      }


   } else {
      outc = base.rgb;
   }




   gl_FragColor=vec4(outc,1.0);

}
