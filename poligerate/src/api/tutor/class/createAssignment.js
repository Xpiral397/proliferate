import axiosClient from "../../axios"


export async function createAssignment() {
    return localStorage.getItem('token')
}

export async function createClasses(obj) {
    const token=JSON.parse(localStorage.getItem('tutor_data')??'{}')?.authentication?.token
    console.log(token, 'kop')
    try {
        const fetch=await axiosClient().post('/tutor/create-assignment/', {
            body: {
                ...obj
            },
            headers: {
                Authorization: `Bearer ${token}`
            }
        })
        return fetch.data
    } catch(e) {
        return {}
    }
}
