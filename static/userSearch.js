const openSearchPopup = document.querySelector('#userSearchOpen')
const userSearchPopup = document.querySelector('#searchUserPopup')
const closeSearchPopup = document.querySelector('#userSearchClose')
const openSearchPopupMobile = document.querySelector('#userSearchOpenMobile')
openSearchPopup.addEventListener('click', () => {
    userSearchPopup.showModal()
})
openSearchPopupMobile.addEventListener('click', () => {
  userSearchPopup.showModal()
})
closeSearchPopup.addEventListener('click', () => {
    userSearchPopup.close()
})

$(document).ready(function () {
    $('#searchUserInput').on('input', function () {
        var query = $(this).val();
        $.ajax({
            type: 'GET',
            url: '/searchUsers',
            data: { query: query },
            success: function (response) {
                $('.searchUserResultsContainer').empty();
                response.forEach(function (user) {
                    var resultHTML = `
                  <a href="/userProfile/@${user.username}">
                    <div class="searchUserResults">
                      <div class="result-image-container">
                        <div class="result-image">
                          <img src="${user.profilePicture}">
                        </div>
                      </div>
                      <div class="result-names">
                        <div class="result-username">
                          <span>@${user.username}</span>
                        </div>
                        <div class="result-name">
                          <span>•</span>
                          <span>${user.name}</span>
                        </div>
                      </div>
                    </div>
                  </a>
                `;
                    $('.searchUserResultsContainer').append(resultHTML);
                });
            },
            error: function (xhr, status, error) {
                console.error('Error searching users:', error);
            }
        });
    });
});