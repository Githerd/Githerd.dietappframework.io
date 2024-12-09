function calculateCalories() {
    setTimeout(() => {
        // Access the form named "tdeeform"
        const form = document.forms["tdeeform"];

        // Determine the gender multiplier (5 for male, -161 for female)
        const gender_value = form.elements["gender"][0].checked ? 5 : -161;

        // Get the activity level multiplier based on the selected option
        const activitylevel_value = [1.2, 1.375, 1.55, 1.725, 1.9][form.elements["activitylevel"].value - 1];

        // Extract weight, height, and age values from the form
        const weight = parseFloat(form.elements["weight"].value) || 0;
        const height = parseFloat(form.elements["height"].value) || 0;
        const age = parseInt(form.elements["age"].value) || 0;

        // Calculate TDEE using the Mifflin-St Jeor Equation
        let calories_result = ((weight * 10) + (height * 6.25) - (5 * age) + gender_value) * activitylevel_value;

        // Ensure the result is non-negative
        calories_result = Math.max(0, calories_result);

        // Display the result in the HTML element with ID 'calories_result'
        document.getElementById('calories_result').innerText = calories_result.toFixed(0);
    }, 1);
}
