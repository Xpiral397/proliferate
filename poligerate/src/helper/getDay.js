// Function to predict the day of the week for a given date
export function getDay(dateString) {
    console.log(dateString)
    const daysOfWeek=['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

    // Split the input dateString into year, month, and day components
    const [year, month, day]=dateString.split('-');

    // Create a new Date object using the parsed components
    const date=new Date(year, month-1, day); // Note: Month is 0-based in JavaScript Date object

    // Get the day of the week (0 = Sunday, 1 = Monday, ..., 6 = Saturday)
    const dayIndex=date.getDay();

    console.log(dayIndex)
    // Return the corresponding day of the week
    return daysOfWeek[dayIndex];
}

// Example usage:
console.log(getDay('2024:04:07')); // Output: 'Sunday'
