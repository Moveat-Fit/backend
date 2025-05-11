# Moveat-Fit | Banco de Dados

## Visão Geral

O script schema.py tem como principais responsabilidades:

* Conectar-se ao servidor MySQL utilizando as credenciais fornecidas no arquivo de ambiente .env.
* Criar a estrutura completa das tabelas necessárias para o funcionamento da aplicação Moveat, caso elas ainda não existam no banco de dados.
* Popular tabelas essenciais com um conjunto de dados iniciais. Isso inclui categorias como grupos alimentares, tipos de refeição, uma lista de nutrientes padrão, e um catálogo base de alimentos comuns com suas respectivas informações nutricionais.
  
__Importante:__ Para garantir que o esquema do banco de dados seja criado exatamente conforme a versão mais recente do schema.py, é recomendado executar o script em um banco de dados limpo ou recém-criado.

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
* `regional_council_number`: Número de registro no conselho regional.
* `created_at`: Data e hora de criação do registro.
* `updated_at`: Data e hora da última atualização do registro.
* **Constraint Única**: `uq_professional_council` (combinação de `regional_council_type` e `regional_council_number` deve ser única).

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
* `weight_kg`: Peso do paciente em quilogramas.
* `height_cm`: Altura do paciente em centímetros.
* `observations`: Observações adicionais sobre o paciente.
* `professional_id`: Identificador do profissional responsável pelo paciente (Chave Estrangeira para `tb_professionals.id`).
* `created_at`: Data e hora de criação do registro.
* `updated_at`: Data e hora da última atualização do registro.

### `tb_food_groups`
Tabela de lookup para categorizar os alimentos (ex: Cereais, Frutas, Vegetais).

* `id`: Identificador único do grupo alimentar (Chave Primária, Auto Incremento).
* `name`: Nome do grupo alimentar (único).

### `tb_nutrients`
Tabela de lookup para os diferentes tipos de nutrientes (ex: Valor Energético, Proteína Total).

* `id`: Identificador único do nutriente (Chave Primária, Auto Incremento).
* `name`: Nome do nutriente (único).
* `unit`: Unidade de medida do nutriente (ex: kcal, g).

### `tb_foods`
Armazena informações detalhadas sobre cada alimento.

* `id`: Identificador único do alimento (Chave Primária, Auto Incremento).
* `name`: Nome do alimento (único).
* `food_group_id`: Identificador do grupo alimentar ao qual o alimento pertence (Chave Estrangeira para `tb_food_groups.id`). Se o grupo for deletado, este campo se torna NULO.
* `default_portion_description`: Descrição da porção padrão do alimento (ex: '1 fatia média').
* `default_portion_grams`: Peso da porção padrão em gramas.

### `tb_food_nutrients`
Tabela de junção que relaciona alimentos aos seus nutrientes, especificando a quantidade de cada nutriente por 100 unidades (gramas ou ml) do alimento.

* `food_id`: Identificador do alimento (Parte da Chave Primária Composta, Chave Estrangeira para `tb_foods.id`). Se o alimento for deletado, as entradas correspondentes aqui são deletadas em cascata.
* `nutrient_id`: Identificador do nutriente (Parte da Chave Primária Composta, Chave Estrangeira para `tb_nutrients.id`). A deleção de um nutriente é restrita se ele estiver em uso aqui.
* `amount_per_100_unit`: Quantidade do nutriente presente em 100 unidades (g/ml) do alimento.

### `tb_meal_types`
Tabela de lookup para os tipos de refeição (ex: Café da Manhã, Almoço, Jantar).

* `id`: Identificador único do tipo de refeição (Chave Primária, Auto Incremento).
* `name`: Nome do tipo de refeição (único).

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
* `meal_type_id`: Identificador do tipo de refeição (Chave Estrangeira para `tb_meal_types.id`). A deleção de um tipo de refeição é restrita se estiver em uso aqui.
* `day_of_plan`: Data específica da refeição dentro do plano.
* `time_scheduled`: Horário agendado para a refeição (opcional).
* `notes`: Observações sobre esta entrada de refeição.
* `created_at`: Data e hora de criação do registro.
* `updated_at`: Data e hora da última atualização do registro.
* **Constraint Única**: `uq_meal_entry` (combinação de `meal_plan_id`, `meal_type_id`, e `day_of_plan` deve ser única).

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
* **Alimentos e Grupos Alimentares**: Um alimento (`tb_foods`) pertence a um grupo alimentar (`tb_food_groups`). Um grupo pode conter vários alimentos.
    * `tb_foods.food_group_id` -> `tb_food_groups.id`
* **Alimentos e Nutrientes**: Um alimento (`tb_foods`) pode ter vários nutrientes (`tb_nutrients`), e um nutriente pode estar presente em vários alimentos. Esta relação muitos-para-muitos é implementada pela tabela `tb_food_nutrients`.
    * `tb_food_nutrients.food_id` -> `tb_foods.id`
    * `tb_food_nutrients.nutrient_id` -> `tb_nutrients.id`
* **Planos Alimentares, Pacientes e Profissionais**: Um plano alimentar (`tb_patient_meal_plans`) é criado por um profissional (`tb_professionals`) para um paciente (`tb_patients`).
    * `tb_patient_meal_plans.patient_id` -> `tb_patients.id`
    * `tb_patient_meal_plans.professional_id` -> `tb_professionals.id`
* **Entradas de Plano Alimentar, Planos e Tipos de Refeição**: Um plano alimentar (`tb_patient_meal_plans`) consiste em várias entradas de refeição (`tb_meal_plan_entries`), cada uma associada a um tipo de refeição (`tb_meal_types`).
    * `tb_meal_plan_entries.meal_plan_id` -> `tb_patient_meal_plans.id`
    * `tb_meal_plan_entries.meal_type_id` -> `tb_meal_types.id`
* **Alimentos em Entradas de Plano, Entradas de Plano e Alimentos**: Cada entrada de refeição (`tb_meal_plan_entries`) pode conter vários alimentos (`tb_foods`), com quantidades específicas definidas em `tb_meal_plan_foods`.
    * `tb_meal_plan_foods.meal_plan_entry_id` -> `tb_meal_plan_entries.id`
    * `tb_meal_plan_foods.food_id` -> `tb_foods.id`

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
  id int [pk, increment]
  full_name varchar(255) [not null, note: "CHECK (CHAR_LENGTH(TRIM(full_name)) > 0)"]
  email varchar(255) [unique, not null, note: "CHECK (email LIKE '%_@__%.__%')"]
  password varchar(255) [not null]
  cpf char(11) [unique, not null]
  phone varchar(20) [not null, note: "CHECK (CHAR_LENGTH(TRIM(phone)) >= 10)"]
  regional_council_type varchar(50) [not null]
  regional_council_number varchar(50) [not null]
  created_at timestamp [default: `CURRENT_TIMESTAMP`]
  updated_at timestamp [default: `CURRENT_TIMESTAMP`, note: "ON UPDATE CURRENT_TIMESTAMP"]

  indexes {
    (regional_council_type, regional_council_number) [unique, name: "uq_professional_council"]
  }
}

Table tb_patients {
  id int [pk, increment]
  full_name varchar(255) [not null, note: "CHECK (CHAR_LENGTH(TRIM(full_name)) > 0)"]
  birth_date date [not null]
  gender gender_enum [not null]
  email varchar(255) [unique, not null, note: "CHECK (email LIKE '%_@__%.__%')"]
  password varchar(255) [not null]
  phone varchar(20) [not null, note: "CHECK (CHAR_LENGTH(TRIM(phone)) >= 10)"]
  cpf char(11) [unique, not null]
  weight_kg decimal(5,2)
  height_cm decimal(5,2)
  observations text
  professional_id int [not null]
  created_at timestamp [default: `CURRENT_TIMESTAMP`]
  updated_at timestamp [default: `CURRENT_TIMESTAMP`, note: "ON UPDATE CURRENT_TIMESTAMP"]
}

Table tb_food_groups {
  id int [pk, increment]
  name varchar(100) [unique, not null]
}

Table tb_nutrients {
  id int [pk, increment]
  name varchar(100) [unique, not null]
  unit varchar(20) [not null]
}

Table tb_foods {
  id int [pk, increment]
  name varchar(255) [unique, not null]
  food_group_id int
  default_portion_description varchar(255)
  default_portion_grams decimal(7,2)
}

Table tb_food_nutrients {
  food_id int [not null]
  nutrient_id int [not null]
  amount_per_100_unit decimal(10,3) [not null]

  indexes {
    (food_id, nutrient_id) [pk]
  }
}

Table tb_meal_types {
  id int [pk, increment]
  name varchar(100) [unique, not null]
}

Table tb_patient_meal_plans {
  id int [pk, increment]
  patient_id int [not null]
  professional_id int [not null]
  plan_name varchar(255) [not null, default: "Plano Nutricional Padrão"]
  start_date date [not null]
  end_date date
  goals text
  created_at timestamp [default: `CURRENT_TIMESTAMP`]
  updated_at timestamp [default: `CURRENT_TIMESTAMP`, note: "ON UPDATE CURRENT_TIMESTAMP"]
}

Table tb_meal_plan_entries {
  id int [pk, increment]
  meal_plan_id int [not null]
  meal_type_id int [not null]
  day_of_plan date [not null]
  time_scheduled time
  notes text
  created_at timestamp [default: `CURRENT_TIMESTAMP`]
  updated_at timestamp [default: `CURRENT_TIMESTAMP`, note: "ON UPDATE CURRENT_TIMESTAMP"]

  indexes {
    (meal_plan_id, meal_type_id, day_of_plan) [unique, name: "uq_meal_entry"]
  }
}

Table tb_meal_plan_foods {
  id int [pk, increment]
  meal_plan_entry_id int [not null]
  food_id int [not null]
  prescribed_quantity_grams decimal(7,2) [not null]
  display_portion varchar(100)
  preparation_notes text
  created_at timestamp [default: `CURRENT_TIMESTAMP`]
  updated_at timestamp [default: `CURRENT_TIMESTAMP`, note: "ON UPDATE CURRENT_TIMESTAMP"]
}

// --- RELACIONAMENTOS ---

Ref: tb_patients.professional_id > tb_professionals.id [delete: restrict]
Ref: tb_foods.food_group_id > tb_food_groups.id [delete: set null]
Ref: tb_food_nutrients.food_id > tb_foods.id [delete: cascade]
Ref: tb_food_nutrients.nutrient_id > tb_nutrients.id [delete: restrict]
Ref: tb_patient_meal_plans.patient_id > tb_patients.id [delete: cascade]
Ref: tb_patient_meal_plans.professional_id > tb_professionals.id [delete: restrict]
Ref: tb_meal_plan_entries.meal_plan_id > tb_patient_meal_plans.id [delete: cascade]
Ref: tb_meal_plan_entries.meal_type_id > tb_meal_types.id [delete: restrict]
Ref: tb_meal_plan_foods.meal_plan_entry_id > tb_meal_plan_entries.id [delete: cascade]
Ref: tb_meal_plan_foods.food_id > tb_foods.id [delete: restrict]

//// -- FIM DO CÓDIGO DBML --
