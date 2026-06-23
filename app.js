const API_URL = "http://127.0.0.1:5000";

loadPatients();

async function loadPatients() {

    try {

        const response = await fetch(`${API_URL}/patients`);
        const patients = await response.json();

        let rows = "";

        patients.forEach(patient => {

            rows += `
            <tr>
                <td>${patient.full_name}</td>
                <td>${patient.date_of_birth}</td>
                <td>${patient.email}</td>
                <td>${patient.glucose}</td>
                <td>${patient.haemoglobin}</td>
                <td>${patient.cholesterol}</td>

                <td>
                    <span class="badge bg-info text-dark">
                        ${patient.remarks}
                    </span>
                </td>

                <td>
                    <button
                        class="btn btn-warning btn-sm"
                        onclick="editPatient(${patient.id})">
                        Edit
                    </button>

                    <button
                        class="btn btn-danger btn-sm"
                        onclick="deletePatient(${patient.id})">
                        Delete
                    </button>
                </td>
            </tr>
            `;
        });

        document.getElementById("patientTable").innerHTML = rows;

    } catch (error) {

        console.error(error);

        alert("Unable to load patients.");

    }
}

document
.getElementById("patientForm")
.addEventListener("submit", async function (e) {

    e.preventDefault();

    const patientId =
        document.getElementById("patientId").value;

    const patient = {

        full_name:
            document.getElementById("full_name").value,

        date_of_birth:
            document.getElementById("date_of_birth").value,

        email:
            document.getElementById("email").value,

        glucose:
            document.getElementById("glucose").value,

        haemoglobin:
            document.getElementById("haemoglobin").value,

        cholesterol:
            document.getElementById("cholesterol").value
    };

    try {

        if (patientId) {

            await fetch(
                `${API_URL}/patients/${patientId}`,
                {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(patient)
                }
            );

            alert("Patient Updated Successfully");

        } else {

            await fetch(
                `${API_URL}/patients`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(patient)
                }
            );

            alert("Patient Saved Successfully");
        }

        this.reset();

        document.getElementById("patientId").value = "";

        loadPatients();

    } catch (error) {

        console.error(error);

        alert("Error while saving patient.");
    }

});

async function editPatient(id) {

    try {

        const response =
            await fetch(`${API_URL}/patients/${id}`);

        const patient =
            await response.json();

        document.getElementById("patientId").value =
            patient.id;

        document.getElementById("full_name").value =
            patient.full_name;

        document.getElementById("date_of_birth").value =
            patient.date_of_birth;

        document.getElementById("email").value =
            patient.email;

        document.getElementById("glucose").value =
            patient.glucose;

        document.getElementById("haemoglobin").value =
            patient.haemoglobin;

        document.getElementById("cholesterol").value =
            patient.cholesterol;

        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });

    } catch (error) {

        console.error(error);

        alert("Unable to load patient details.");
    }
}

async function deletePatient(id) {

    if (!confirm("Are you sure you want to delete this patient?")) {
        return;
    }

    try {

        await fetch(
            `${API_URL}/patients/${id}`,
            {
                method: "DELETE"
            }
        );

        alert("Patient Deleted Successfully");

        loadPatients();

    } catch (error) {

        console.error(error);

        alert("Unable to delete patient.");
    }
}
