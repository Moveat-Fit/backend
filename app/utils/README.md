# Moveat-Fit | Banco de Dados

## Visão Geral

O script schema.py tem como principais responsabilidades:

* Conectar-se ao servidor MySQL utilizando as credenciais fornecidas no arquivo de ambiente .env.
* Criar a estrutura completa das tabelas necessárias para o funcionamento da aplicação Moveat, caso elas ainda não existam no banco de dados.
* Popular a tabela `tb_foods` com um conjunto de dados iniciais, incluindo um catálogo base de alimentos comuns com suas respectivas informações de grupo alimentar, porção padrão e valor energético para essa porção.
  
__Importante:__ Para garantir que o esquema do banco de dados seja criado exatamente conforme a versão mais recente do schema.py, é fundamental executar o script. O script foi projetado para remover e recriar tabelas.

## Descrição das Tabelas

### `tb_professionals`
Armazena informações sobre os profissionais de nutrição cadastrados.

* `id`: Identificador único do profissional (Chave Primária, Auto Incremento).
* `full_name`: Nome completo do profissional.
* `email`: Endereço de e-mail único do profissional.
* `password`: Senha criptografada do profissional.
* `cpf`: CPF único do profissional.
* `phone`: Número de telefone do profissional.
* `regional_council_type`: Tipo de conselho regional (ex: CRN ou CREF).
* `regional_council`: Número de registro no conselho regional.
* `created_at`: Data e hora de criação do registro.
* `updated_at`: Data e hora da última atualização do registro.

### `tb_patients`
Armazena informações sobre os pacientes vinculados aos profissionais.

* `id`: Identificador único do paciente (Chave Primária, Auto Incremento).
* `full_name`: Nome completo do paciente.
* `birth_date`: Data de nascimento do paciente.
* `gender`: Gênero do paciente ('M', 'F', 'Other').
* `email`: Endereço de e-mail único do paciente.
* `password`: Senha criptografada do paciente.
* `phone`: Número de telefone do paciente.
* `cpf`: CPF único do paciente.
* `weight`: Peso do paciente.
* `height`: Altura do paciente.
* `note`: Observações adicionais sobre o paciente.
* `professional_id`: Identificador do profissional responsável pelo paciente (Chave Estrangeira para `tb_professionals.id`).
* `created_at`: Data e hora de criação do registro.
* `updated_at`: Data e hora da última atualização do registro.

### `tb_foods`
Armazena informações detalhadas sobre cada alimento.

* `id`: Identificador único do alimento (Chave Primária, Auto Incremento).
* `name`: Nome do alimento (único).
* `food_group_name`: Nome do grupo alimentar ao qual o alimento pertence (ex: 'Cereais', 'Frutas').
* `default_portion_description`: Descrição da porção padrão do alimento (ex: '1 fatia média').
* `default_portion_grams`: Peso da porção padrão em gramas.
* `energy_value_kcal`: Valor energético (em kcal) referente à default_portion_grams do alimento.

### `tb_patient_meal_plans`
Armazena os planos alimentares criados para os pacientes.

* `id`: Identificador único do plano alimentar (Chave Primária, Auto Incremento).
* `patient_id`: Identificador do paciente ao qual o plano se destina (Chave Estrangeira para `tb_patients.id`). Se o paciente for deletado, seus planos são deletados em cascata.
* `professional_id`: Identificador do profissional que criou o plano (Chave Estrangeira para `tb_professionals.id`). A deleção de um profissional é restrita se ele tiver planos associados.
* `plan_name`: Nome do plano alimentar (padrão: 'Plano Nutricional Padrão').
* `start_date`: Data de início do plano.
* `end_date`: Data de término do plano (opcional).
* `goals`: Objetivos do plano alimentar.
* `created_at`: Data e hora de criação do registro.
* `updated_at`: Data e hora da última atualização do registro.

### `tb_meal_plan_entries`
Define as entradas específicas de refeições dentro de um plano alimentar para um determinado dia.

* `id`: Identificador único da entrada do plano (Chave Primária, Auto Incremento).
* `meal_plan_id`: Identificador do plano alimentar ao qual esta entrada pertence (Chave Estrangeira para `tb_patient_meal_plans.id`). Se o plano for deletado, suas entradas são deletadas em cascata.
* `meal_type_name`: Nome do tipo da refeição, definido livremente pelo nutricionista (ex: "Café da Manhã", "Ceia", "Pré-treino")
* `day_of_plan`: Data específica da refeição dentro do plano.
* `time_scheduled`: Horário agendado para a refeição (opcional).
* `notes`: Observações sobre esta entrada de refeição.
* `created_at`: Data e hora de criação do registro.
* `updated_at`: Data e hora da última atualização do registro.

### `tb_meal_plan_foods`
Tabela de junção que detalha os alimentos específicos e suas quantidades prescritas para cada entrada de refeição em um plano.

* `id`: Identificador único do alimento no plano (Chave Primária, Auto Incremento).
* `meal_plan_entry_id`: Identificador da entrada do plano de refeição à qual este alimento pertence (Chave Estrangeira para `tb_meal_plan_entries.id`). Se a entrada do plano for deletada, os alimentos associados são deletados em cascata.
* `food_id`: Identificador do alimento (Chave Estrangeira para `tb_foods.id`). A deleção de um alimento é restrita se ele estiver em uso aqui.
* `prescribed_quantity_grams`: Quantidade prescrita do alimento em gramas.
* `display_portion`: Descrição da porção para exibição (ex: '1 concha média', '2 unidades').
* `preparation_notes`: Notas sobre o preparo do alimento.
* `created_at`: Data e hora de criação do registro.
* `updated_at`: Data e hora da última atualização do registro.

## Relacionamentos Principais

* **Profissional e Pacientes**: Um profissional (`tb_professionals`) pode ter vários pacientes (`tb_patients`), mas um paciente está associado a apenas um profissional.
    * `tb_patients.professional_id` -> `tb_professionals.id`
* **Planos Alimentares, Pacientes e Profissionais**: Um plano alimentar (`tb_patient_meal_plans`) é criado por um profissional (`tb_professionals`) para um paciente (`tb_patients`).
    * `tb_patient_meal_plans.patient_id` -> `tb_patients.id`
    * `tb_patient_meal_plans.professional_id` -> `tb_professionals.id`
* **Entradas de Plano Alimentar e Planos**: Um plano alimentar (`tb_patient_meal_plans`) consiste em várias entradas de refeição (`tb_meal_plan_entries`).
    * `tb_meal_plan_entries.meal_plan_id` -> `tb_patient_meal_plans.id`
* **Alimentos em Entradas de Plano, Entradas de Plano e Alimentos**: Cada entrada de refeição (`tb_meal_plan_entries`) pode conter vários alimentos (`tb_foods`), com quantidades específicas definidas em      `tb_meal_plan_foods`.
    * `tb_meal_plan_foods.meal_plan_entry_id` -> `tb_meal_plan_entries.id`
    * `tb_meal_plan_foods.food_id`-> `tb_foods.id`

    ## Diagrama Entidade-Relacionamento (DER) - DBML

O esquema do banco de dados pode ser visualizado usando a sintaxe DBML (Database Markup Language). 

Você pode acessar o diagrama visual [aqui](https://dbdiagram.io/d/67b51690263d6cf9a0a29350) ou copiar o código abaixo e colá-lo em [dbdiagram.io](https://dbdiagram.io/).


```dbml
//// -- INÍCIO DO CÓDIGO DBML --

Enum gender_enum {
  M
  F
  Other
}

Table tb_professionals {
  id int [pk, increment, note: 'Identificador único do profissional']
  full_name varchar(255) [not null, note: 'Nome completo. CHECK: CHAR_LENGTH(TRIM(full_name)) > 0']
  email varchar(255) [unique, not null, note: "Email único. CHECK: email LIKE '%_@__%.__%'"]
  password varchar(255) [not null, note: 'Senha (deve ser armazenada com hash)']
  cpf char(11) [unique, not null, note: 'CPF único']
  phone varchar(15) [not null, note: 'Telefone. CHECK: CHAR_LENGTH(TRIM(phone)) >= 10']
  regional_council_type varchar(50) [not null, note: 'Tipo do conselho regional (ex: CRN)']
  regional_council varchar(50) [not null, note: 'Número de registro no conselho regional']
  created_at timestamp [default: `CURRENT_TIMESTAMP`, note: 'Data de criação']
  updated_at timestamp [default: `CURRENT_TIMESTAMP`, note: 'Data da última atualização (MySQL: ON UPDATE CURRENT_TIMESTAMP)']

  Indexes {
    (regional_council_type, regional_council) [unique, name: 'uq_professional_council']
  }
  note: 'Profissionais de nutrição cadastrados.'
}

Table tb_patients {
  id int [pk, increment, note: 'Identificador único do paciente']
  full_name varchar(255) [not null, note: 'Nome completo. CHECK: CHAR_LENGTH(TRIM(full_name)) > 0']
  birth_date date [not null, note: 'Data de nascimento']
  gender gender_enum [not null, note: 'Gênero']
  email varchar(255) [unique, not null, note: "Email único. CHECK: email LIKE '%_@__%.__%'"]
  password varchar(255) [not null, note: 'Senha (deve ser armazenada com hash)']
  phone varchar(15) [not null, note: 'Telefone. CHECK: CHAR_LENGTH(TRIM(phone)) >= 10']
  cpf char(11) [unique, not null, note: 'CPF único']
  weight decimal(5,2) [not null, note: 'Peso do paciente']
  height decimal(3,2) [not null, note: 'Altura do paciente']
  note text [note: 'Observações adicionais sobre o paciente']
  professional_id int [not null, note: 'ID do profissional responsável']
  created_at timestamp [default: `CURRENT_TIMESTAMP`, note: 'Data de criação']
  updated_at timestamp [default: `CURRENT_TIMESTAMP`, note: 'Data da última atualização (MySQL: ON UPDATE CURRENT_TIMESTAMP)']
  note: 'Pacientes cadastrados e vinculados a profissionais.'
}

Table tb_foods {
  id int [pk, increment, note: 'ID do alimento']
  name varchar(255) [unique, not null, note: 'Nome do alimento']
  food_group_name varchar(100) [note: 'Nome do grupo alimentar (ex: Cereais, Frutas)']
  default_portion_description varchar(255) [note: 'Descrição da porção padrão (ex: 1 xícara)']
  default_portion_grams decimal(7,2) [note: 'Peso em gramas da porção padrão']
  energy_value_kcal decimal(7,2) [note: 'Valor energético (kcal) para a porção padrão (default_portion_grams)']
  note: 'Catálogo de alimentos com informação nutricional básica (valor energético da porção padrão).'
}

Table tb_patient_meal_plans {
  id int [pk, increment, note: 'ID do plano alimentar']
  patient_id int [not null, note: 'ID do paciente']
  professional_id int [not null, note: 'ID do profissional']
  plan_name varchar(255) [not null, default: 'Plano Nutricional Padrão', note: 'Nome do plano']
  start_date date [not null, note: 'Data de início do plano']
  end_date date [note: 'Data de término do plano (opcional)']
  goals text [note: 'Objetivos do plano']
  created_at timestamp [default: `CURRENT_TIMESTAMP`, note: 'Data de criação']
  updated_at timestamp [default: `CURRENT_TIMESTAMP`, note: 'Data da última atualização (MySQL: ON UPDATE CURRENT_TIMESTAMP)']
  note: 'Planos alimentares dos pacientes.'
}

Table tb_meal_plan_entries {
  id int [pk, increment, note: 'ID da entrada da refeição no plano']
  meal_plan_id int [not null, note: 'ID do plano alimentar']
  meal_type_name varchar(100) [not null, note: 'Nome/tipo da refeição (ex: Café da Manhã, Ceia)']
  day_of_plan date [not null, note: 'Data da refeição no plano']
  time_scheduled time [note: 'Horário agendado (opcional)']
  notes text [note: 'Observações sobre a refeição']
  created_at timestamp [default: `CURRENT_TIMESTAMP`, note: 'Data de criação']
  updated_at timestamp [default: `CURRENT_TIMESTAMP`, note: 'Data da última atualização (MySQL: ON UPDATE CURRENT_TIMESTAMP)']

  Indexes {
    (meal_plan_id, meal_type_name, day_of_plan) [unique, name: 'uq_meal_entry']
  }
  note: 'Entradas de refeições (ex: Café da Manhã de Segunda) em um plano.'
}

Table tb_meal_plan_foods {
  id int [pk, increment, note: 'ID do alimento na refeição do plano']
  meal_plan_entry_id int [not null, note: 'ID da entrada da refeição']
  food_id int [not null, note: 'ID do alimento']
  prescribed_quantity_grams decimal(7,2) [not null, note: 'Quantidade prescrita em gramas']
  display_portion varchar(100) [note: 'Descrição da porção para exibição (ex: 1 unidade)']
  preparation_notes text [note: 'Notas de preparo']
  created_at timestamp [default: `CURRENT_TIMESTAMP`, note: 'Data de criação']
  updated_at timestamp [default: `CURRENT_TIMESTAMP`, note: 'Data da última atualização (MySQL: ON UPDATE CURRENT_TIMESTAMP)']
  note: 'Alimentos específicos e suas quantidades em cada refeição do plano.'
}

// --- RELACIONAMENTOS ---

Ref: tb_patients.professional_id > tb_professionals.id [delete: restrict]

Ref: tb_patient_meal_plans.patient_id > tb_patients.id [delete: cascade]
Ref: tb_patient_meal_plans.professional_id > tb_professionals.id [delete: restrict]

Ref: tb_meal_plan_entries.meal_plan_id > tb_patient_meal_plans.id [delete: cascade]

Ref: tb_meal_plan_foods.meal_plan_entry_id > tb_meal_plan_entries.id [delete: cascade]
Ref: tb_meal_plan_foods.food_id > tb_foods.id [delete: restrict]

//// -- FIM DO CÓDIGO DBML --