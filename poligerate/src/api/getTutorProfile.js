import axiosClient from "./axios"

export  function getToken() {
    return localStorage.getItem('tokens')
}

export async function useTutorProfile() {
    const token=getToken()
        // JSON.parse(localStorage.getItem('tutor_data')??'{}')?.authentication?.token
    console.log(token, 'kop')
    try {
        const fetch = await axiosClient().get('/tutor/get-tutor-profile/', {
            headers: {
                Authorization: `Bearer ${token}`
            }
        })
        return fetch.data()
    }
    catch(e) {
        return {
            
        }
    }

}
