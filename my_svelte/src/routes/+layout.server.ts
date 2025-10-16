/*import type{LayoutServerLoad} from './$types';
import {redirect} from '@sveltejs/kit';
import axios from "axios";

export const load: LayoutServerLoad = async ({ cookies, url  }) => {
  const token = cookies.get('token'); 
  let rol = 0;

  // rutas de visitantes 
  const rutasVisit = ['/','/howstart','/login','/registro'];
  if(rutasVisit.includes(url.pathname)){
    return{ token:null, rol:0};
  }
  if(!token){
    throw redirect(303,'/login');
  }
   try {
        // Verificamos el token con FastAPI
        const res = await axios.get('http://127.0.0.1:8000/verify_token', {
            headers: { Authorization: `Bearer ${token}` }
        });
        rol = res.data.rol;
    } catch (err) {
        console.error('Token inválido o sesión expirada');
        // token  inválido o expirado  redirige al login
        throw redirect(303, '/login');
    }
  return { token, rol };
}; */