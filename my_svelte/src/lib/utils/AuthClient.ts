import { browser } from '$app/environment';

// ================================
// CONFIGURACIÓN
// ================================
const API_BASE_URL = 'http://127.0.0.1:8000';

// ================================
// TIPOS
// ================================
export interface UserData {
    id: number;
    name: string;
    email: string;
    rol: number;
    [key: string]: any; // Para campos adicionales
}

// ================================
// UTILIDADES PRIVADAS
// ================================
/**
 * Redirige al usuario a la página de login y muestra un mensaje
 */
function redirectToLogin(message: string = "No tienes sesión iniciada"): void {
    if (!browser) return;

    alert(message);
    window.location.href = "/login";
}

// ================================
// FUNCIONES PÚBLICAS
// ================================

/**
 * Cierra la sesión del usuario eliminando el token y redirigiendo al inicio
 */
export function cerrarSesion(): void {
    if (!browser) return; // Evita errores en SSR

    try {
        localStorage.removeItem("token");
        window.location.href = "/";
    } catch (error) {
        console.error("Error al cerrar sesión:", error);
    }
}

/**
 * Obtiene el token del localStorage
 * @returns El token o null si no existe
 */
export function getToken(): string | null {
    if (!browser) return null;
    return localStorage.getItem("token");
}

/**
 * Guarda el token en el localStorage
 * @param token - Token JWT a guardar
 */
export function setToken(token: string): void {
    if (!browser) return;
    localStorage.setItem("token", token);
}

/**
 * Verifica si el token es válido consultando al backend
 * Si el token es inválido o no existe, redirige a login
 * @returns Los datos del usuario o null si no hay sesión válida
 */
export async function verifyToken(): Promise<UserData | null> {
    if (!browser) return null; // Evita errores en SSR

    const token = getToken();

    if (!token) {
        redirectToLogin();
        return null;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/Login/verify_token/${token}`);

        if (!response.ok) {
            // Token inválido o expirado
            if (response.status === 401 || response.status === 403) {
                redirectToLogin("Tu sesión ha expirado. Por favor, inicia sesión nuevamente.");
            } else {
                redirectToLogin("Error al verificar tu sesión.");
            }
            return null;
        }

        const data: UserData = await response.json();
        return data;

    } catch (error) {
        console.error("Error al verificar el token:", error);
        redirectToLogin("Error de conexión. Por favor, intenta de nuevo.");
        return null;
    }
}
