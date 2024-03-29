import axiosClient from "../../axios"



export async function getAssignment(obj) {
    const token=JSON.parse(localStorage.getItem('tutor_data')??'{}')?.authentication?.token
    console.log(token, 'kop')
    try {
        const fetch=await axiosClient().get('/tutor/get-my-assignments/', {
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
