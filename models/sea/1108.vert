#version 120

vec4 _l_color1;
vec4 _l_position1;
vec2 _l_texcoord11;
vec2 _l_alpha_uv1;
vec2 _l_texcoord01;
vec2 _l_interpolate1;
float _TMP3;
float _TMP2;
uniform vec4 lightposition;
uniform vec4 ambientcolor;
uniform vec4 diffusecolor;
uniform vec4 lightparameters;
uniform vec4 fogexpdensity;
uniform vec4 map;
uniform vec4 alphamap;
uniform vec4 trans_view_to_world[4];
uniform vec4 trans_model_to_view[4];
uniform vec4 trans_model_to_apiclip[4];
vec4 _r0017;
vec4 _r0027;
vec4 _r0037;
float _TMP46;
float _x0047;
vec4 _r0051;
vec3 _v0061;
vec3 _v0067;

 // main procedure, the original name was vshader
void main()
{

    vec4 _vertex;
    float _diffuse;
    vec3 _light_direction;
    vec3 _opposite_light_direction;

    _vertex.xyz = gl_Vertex.xyz;
    _vertex.w = 1.00000000E+00;
    _r0017.x = dot(trans_model_to_apiclip[0], _vertex);
    _r0017.y = dot(trans_model_to_apiclip[1], _vertex);
    _r0017.z = dot(trans_model_to_apiclip[2], _vertex);
    _r0017.w = dot(trans_model_to_apiclip[3], _vertex);
    _l_texcoord01 = gl_MultiTexCoord0.xy;
    _r0027.x = dot(trans_model_to_view[0], _vertex);
    _r0027.y = dot(trans_model_to_view[1], _vertex);
    _r0027.z = dot(trans_model_to_view[2], _vertex);
    _r0027.w = dot(trans_model_to_view[3], _vertex);
    _r0037.x = dot(trans_view_to_world[0], _r0027);
    _r0037.y = dot(trans_view_to_world[1], _r0027);
    _l_interpolate1.xy = (_r0037.xy - map.xy)*map.zw;
    _l_alpha_uv1.xy = (_r0037.xy - alphamap.xy)*alphamap.zw;
    _x0047 = -(fogexpdensity.x*_r0027.y);
    _TMP46 = pow(2.71828198E+00, _x0047);
    _l_color1.w = 1.00000000E+00 - _TMP46;
    _r0051.x = dot(vec4( 5.00000000E-01, 0.00000000E+00, 0.00000000E+00, 5.00000000E-01), _r0017);
    _r0051.y = dot(vec4( 0.00000000E+00, 5.00000000E-01, 0.00000000E+00, 5.00000000E-01), _r0017);
    _r0051.w = dot(vec4( 0.00000000E+00, 0.00000000E+00, 0.00000000E+00, 1.00000000E+00), _r0017);
    _l_texcoord11.xy = _r0051.xy/_r0051.w;
    _v0061 = gl_Vertex.xyz - lightposition.xyz;
    _TMP2 = dot(_v0061, _v0061);
    _TMP3 = inversesqrt(_TMP2);
    _light_direction = _TMP3*_v0061;
    _v0067 = -_light_direction;
    _TMP2 = dot(_v0067, _v0067);
    _TMP3 = inversesqrt(_TMP2);
    _opposite_light_direction = _TMP3*_v0067;
    _diffuse = dot(gl_Normal, _opposite_light_direction);
    _l_color1.xyz = diffusecolor.xyz*_diffuse*lightparameters.x + ambientcolor.xyz;
    _l_position1 = _r0017;
    gl_TexCoord[2].xy = _l_interpolate1;
    gl_TexCoord[0].xy = gl_MultiTexCoord0.xy;
    gl_TexCoord[3].xy = _l_alpha_uv1;
    gl_TexCoord[1].xy = _l_texcoord11;
    gl_Position = _r0017;
    gl_FrontColor = _l_color1;
} // main end