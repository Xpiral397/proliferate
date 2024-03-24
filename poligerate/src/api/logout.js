export function Logout(Provider) {
    switch (Provider) {
        case "TUTOR":
            localStorage.setItem("tutor_data", '')
    }
}