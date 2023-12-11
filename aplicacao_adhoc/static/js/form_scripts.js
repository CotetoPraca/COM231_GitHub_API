$(document).ready(function() {
  $('input[name="query_type"]').change(function() {
    var selectedOption = $(this).val();
    console.log('selectedOption:', selectedOption);

    if (selectedOption === 'list_users') {
      $("#userAccountFieldsForm").show();
    } else {
      $("#userAccountFieldsForm").hide();
    }

    if (selectedOption === 'select_user') {
      $("#userAccountSingleUserForm").show();
    } else {
      $("#userAccountSingleUserForm").hide();
    }

    if (selectedOption === 'multi_table_search') {
      $("#userAccountMultiTableSearch").show();
    } else {
      $("#userAccountMultiTableSearch").hide();
    }
  });

  // // Mostra a tabela quando o formulário é submetido
  // $('form').submit(function() {
  //   initDataTable();
  // });

  // // Função para inicializar o DataTable
  // function initDataTable() {
  //   // Destrói o DataTable se já estiver inicializado
  //   if ($.fn.DataTable.isDataTable('#userAccountTable')) {
  //     $('#userAccountTable').DataTable().destroy();
  //   }

  //   // Inicializa o DataTable apenas se houver dados na tabela
  //   if ($('#userAccountTable tbody tr').length > 0) {
  //     $('#userAccountTable').DataTable();
  //   }
  // }
});
