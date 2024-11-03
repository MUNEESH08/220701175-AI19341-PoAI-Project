$(document).ready(function(){
    function getInfo() {
        let regno = $('#regno').val();
        $.ajax({
            url: '/details',
            method: 'POST',
            data: { regno: regno },
            success: function(response) {
                if (response.student) {
                    $('#rollNo').text(response.student.roll_no);
                    $('#name').text(response.student.name);
                    $('#company').text(response.student.company);
                    $('#campusStatus').text(response.student.campus_status);
                    $('#lpa').text(response.student.lpa);
                    $('#cgpa').text(response.student.cgpa);
                    $('#batch').text(response.student.batch);
                    if (response.student.campus_status === 'HIGHER EDUCATION') {
                        $('#companyLabel').text('University:');
                    } else {
                        $('#companyLabel').text('Company Employed:');
                    }
                    $('#studentDetails').show();
                    $('#errorMessage').text('');
                } else if (response.error) {
                    $('#errorMessage').text(response.error);
                    $('#studentDetails').hide();
                    $('#imageContainer').hide();
                }
            }
        });
    }

    // Trigger form submission when pressing Enter
    $('#regno').keypress(function (e) {
        if (e.which == 13) {
            e.preventDefault(); // Prevent the default form submission
            getInfo(); // Call the function to get info
        }
    });

    // Trigger form submission on button click
    $('#getInfoBtn').on('click', function(){
        getInfo();
    });
});
