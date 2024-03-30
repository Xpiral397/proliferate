export function getUserToken() {
    return localStorage.getItem('token_data')??""
}

export function StoreUserTokne(token){
    return localStorage.setItem('userToken',token)
}
export function clearUserTone() {
    return localStorage.removeItem('userToken')
}