import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()


def connect_database():

    try:
        cnxn = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DB"),
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci'
        )
        print("Conexão estabelecida.")
        return cnxn
    except mysql.connector.Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None


def create_tables(cnxn):
    if cnxn is None:
        print("Não foi possível criar as tabelas, pois a conexão falhou.")
        return

    sql_commands = [
        """
        CREATE TABLE IF NOT EXISTS tb_professionals (
            id INT AUTO_INCREMENT PRIMARY KEY,
            full_name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            cpf CHAR(11) UNIQUE NOT NULL,
            phone VARCHAR(20) NOT NULL,
            regional_council_type VARCHAR(50) NOT NULL,
            regional_council_number VARCHAR(50) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            CONSTRAINT uq_professional_council UNIQUE (regional_council_type, regional_council_number),
            CONSTRAINT chk_prof_full_name CHECK (CHAR_LENGTH(TRIM(full_name)) > 0),
            CONSTRAINT chk_prof_email CHECK (email LIKE '%_@__%.__%'),
            CONSTRAINT chk_prof_phone CHECK (CHAR_LENGTH(TRIM(phone)) >= 10)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """,
        """
        CREATE TABLE IF NOT EXISTS tb_patients (
            id INT AUTO_INCREMENT PRIMARY KEY,
            full_name VARCHAR(255) NOT NULL,
            birth_date DATE NOT NULL,
            gender ENUM('M', 'F', 'Other') NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            phone VARCHAR(20) NOT NULL,
            cpf CHAR(11) UNIQUE NOT NULL,
            weight_kg DECIMAL(5,2),
            height_cm DECIMAL(5,2),
            observations TEXT,
            professional_id INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (professional_id) REFERENCES tb_professionals(id) ON DELETE RESTRICT,
            CONSTRAINT chk_patient_full_name CHECK (CHAR_LENGTH(TRIM(full_name)) > 0),
            CONSTRAINT chk_patient_email CHECK (email LIKE '%_@__%.__%'),
            CONSTRAINT chk_patient_phone CHECK (CHAR_LENGTH(TRIM(phone)) >= 10)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """,
        """
        CREATE TABLE IF NOT EXISTS tb_food_groups (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """,
        """
        CREATE TABLE IF NOT EXISTS tb_nutrients (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE,
            unit VARCHAR(20) NOT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """,
        """
        CREATE TABLE IF NOT EXISTS tb_foods (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL UNIQUE,
            food_group_id INT,
            default_portion_description VARCHAR(255),
            default_portion_grams DECIMAL(7,2) NULL,
            FOREIGN KEY (food_group_id) REFERENCES tb_food_groups(id) ON DELETE SET NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """,
        """
        CREATE TABLE IF NOT EXISTS tb_food_nutrients (
            food_id INT NOT NULL,
            nutrient_id INT NOT NULL,
            amount_per_100_unit DECIMAL(10,3) NOT NULL,
            PRIMARY KEY (food_id, nutrient_id),
            FOREIGN KEY (food_id) REFERENCES tb_foods(id) ON DELETE CASCADE,
            FOREIGN KEY (nutrient_id) REFERENCES tb_nutrients(id) ON DELETE RESTRICT
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """,
        """
        CREATE TABLE IF NOT EXISTS tb_meal_types (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """,
        """
        CREATE TABLE IF NOT EXISTS tb_patient_meal_plans (
            id INT AUTO_INCREMENT PRIMARY KEY,
            patient_id INT NOT NULL,
            professional_id INT NOT NULL,
            plan_name VARCHAR(255) NOT NULL DEFAULT 'Plano Nutricional Padrão',
            start_date DATE NOT NULL,
            end_date DATE,
            goals TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES tb_patients(id) ON DELETE CASCADE,
            FOREIGN KEY (professional_id) REFERENCES tb_professionals(id) ON DELETE RESTRICT
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """,
        """
        CREATE TABLE IF NOT EXISTS tb_meal_plan_entries (
            id INT AUTO_INCREMENT PRIMARY KEY,
            meal_plan_id INT NOT NULL,
            meal_type_id INT NOT NULL,
            day_of_plan DATE NOT NULL,
            time_scheduled TIME NULL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (meal_plan_id) REFERENCES tb_patient_meal_plans(id) ON DELETE CASCADE,
            FOREIGN KEY (meal_type_id) REFERENCES tb_meal_types(id) ON DELETE RESTRICT,
            UNIQUE KEY uq_meal_entry (meal_plan_id, meal_type_id, day_of_plan)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """,
        """
        CREATE TABLE IF NOT EXISTS tb_meal_plan_foods (
            id INT AUTO_INCREMENT PRIMARY KEY,
            meal_plan_entry_id INT NOT NULL,
            food_id INT NOT NULL,
            prescribed_quantity_grams DECIMAL(7,2) NOT NULL,
            display_portion VARCHAR(100),
            preparation_notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (meal_plan_entry_id) REFERENCES tb_meal_plan_entries(id) ON DELETE CASCADE,
            FOREIGN KEY (food_id) REFERENCES tb_foods(id) ON DELETE RESTRICT
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
    ]

    try:
        cursor = cnxn.cursor()
        for command in sql_commands:
            try:
                cursor.execute(command)
            except mysql.connector.Error as e:
                print(
                    f"Erro ao executar comando: {command.strip()[:100]}... \nERRO: {e}")
        cnxn.commit()
        print("Tabelas criadas com sucesso.")
    except mysql.connector.Error as e:
        print(f"Erro geral ao criar as tabelas: {e}")
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()


def insert_initial_data(cnxn):
    """Insere dados iniciais em tabelas de lookup e alimentos com suas informações nutricionais."""
    if cnxn is None:
        print("Não foi possível inserir os dados iniciais, pois a conexão falhou.")
        return

    insert_commands = [
        # --- GRUPOS ALIMENTARES ---
        """
        INSERT IGNORE INTO tb_food_groups (name) VALUES
        ('Cereais'),
        ('Frutas'),
        ('Vegetais'),
        ('Proteínas'),
        ('Laticínios'),
        ('Gorduras'),
        ('Açúcares')
        """,
        # --- TIPOS DE REFEIÇÃO ---
        """
        INSERT IGNORE INTO tb_meal_types (name) VALUES
        ('Café da Manhã'),
        ('Almoço'),
        ('Lanche da Tarde'),
        ('Jantar')
        """,
        # --- NUTRIENTES ---
        """
        INSERT IGNORE INTO tb_nutrients (name, unit) VALUES
        ('Valor Energético', 'kcal'),
        ('Proteína Total', 'g'),
        ('Carboidrato Total', 'g'),
        ('Gorduras Totais', 'g'),
        ('Açúcares Totais', 'g')
        """,

        # --- ALIMENTOS ---
        # Cereais
        """
        INSERT IGNORE INTO tb_foods (name, food_group_id, default_portion_description, default_portion_grams) VALUES
        ('Feijão carioca cozido', (SELECT id from tb_food_groups WHERE name='Vegetais'), '60g', 60.0),
        ('Arroz branco cozido', (SELECT id from tb_food_groups WHERE name='Cereais'), '50g', 50.0),
        ('Batata inglesa cozida', (SELECT id from tb_food_groups WHERE name='Cereais'), '100g', 100.0),
        ('Batata doce cozida', (SELECT id from tb_food_groups WHERE name='Cereais'), '100g', 100.0),
        ('Macarrão cozido', (SELECT id from tb_food_groups WHERE name='Cereais'), '80g (peso cozido)', 80.0),
        ('Pão francês', (SELECT id from tb_food_groups WHERE name='Cereais'), '1 unidade (50g)', 50.0),
        ('Pão de forma tradicional', (SELECT id from tb_food_groups WHERE name='Cereais'), '2 fatias (50g)', 50.0),
        ('Goma de tapioca', (SELECT id from tb_food_groups WHERE name='Cereais'), '100g (peso seco)', 100.0);
        """,
        # Vegetais
        """
        INSERT IGNORE INTO tb_foods (name, food_group_id, default_portion_description, default_portion_grams) VALUES
        ('Abóbora cozida', (SELECT id from tb_food_groups WHERE name='Vegetais'), '100g', 100.0),
        ('Berinjela cozida', (SELECT id from tb_food_groups WHERE name='Vegetais'), '100g', 100.0),
        ('Cenoura cozida', (SELECT id from tb_food_groups WHERE name='Vegetais'), '100g', 100.0),
        ('Beterraba cozida', (SELECT id from tb_food_groups WHERE name='Vegetais'), '100g', 100.0),
        ('Brócolis cozido', (SELECT id from tb_food_groups WHERE name='Vegetais'), '100g', 100.0);
        """,
        # Frutas
        """
        INSERT IGNORE INTO tb_foods (name, food_group_id, default_portion_description, default_portion_grams) VALUES
        ('Melão', (SELECT id from tb_food_groups WHERE name='Frutas'), '1 fatia média (100g)', 100.0),
        ('Melancia', (SELECT id from tb_food_groups WHERE name='Frutas'), '1 fatia média (100g)', 100.0),
        ('Morango', (SELECT id from tb_food_groups WHERE name='Frutas'), '1 xícara (100g)', 100.0),
        ('Abacaxi', (SELECT id from tb_food_groups WHERE name='Frutas'), '1 fatia média (100g)', 100.0),
        ('Kiwi', (SELECT id from tb_food_groups WHERE name='Frutas'), '1 unidade média (100g)', 100.0),
        ('Uva', (SELECT id from tb_food_groups WHERE name='Frutas'), '1 cacho pequeno (100g)', 100.0);
        """,
        # Proteínas
        """
        INSERT IGNORE INTO tb_foods (name, food_group_id, default_portion_description, default_portion_grams) VALUES
        ('Ovos de galinha, cozidos', (SELECT id from tb_food_groups WHERE name='Proteínas'), '1 unidade grande (50g)', 50.0),
        ('Frango grelhado (peito)', (SELECT id from tb_food_groups WHERE name='Proteínas'), '1 filé (100g)', 100.0),
        ('Patinho bovino, grelhado/moído', (SELECT id from tb_food_groups WHERE name='Proteínas'), '1 porção (100g)', 100.0),
        ('Tilápia cozida (filé)', (SELECT id from tb_food_groups WHERE name='Proteínas'), '1 filé (100g)', 100.0),
        ('Whey Protein Concentrado (pó)', (SELECT id from tb_food_groups WHERE name='Proteínas'), '1 scoop (30g)', 30.0);
        """,
        # Laticínios
        """
        INSERT IGNORE INTO tb_foods (name, food_group_id, default_portion_description, default_portion_grams) VALUES
        ('Iogurte desnatado (Zero)', (SELECT id from tb_food_groups WHERE name='Laticínios'), '1 pote (170g)', 170.0),
        ('Requeijão cremoso light', (SELECT id from tb_food_groups WHERE name='Laticínios'), '1 colher de sopa (30g)', 30.0),
        ('Margarina com sal', (SELECT id from tb_food_groups WHERE name='Gorduras'), '1 colher de chá (10g)', 10.0);
        """,
        # Gorduras
        """
        INSERT IGNORE INTO tb_foods (name, food_group_id, default_portion_description, default_portion_grams) VALUES
        ('Azeite de oliva extra virgem', (SELECT id from tb_food_groups WHERE name='Gorduras'), '1 colher de sopa (13ml)', 11.96),
        ('Pasta de Amendoim integral', (SELECT id from tb_food_groups WHERE name='Gorduras'), '1 colher de sopa (15g)', 15.0),
        ('Castanha do Pará', (SELECT id from tb_food_groups WHERE name='Gorduras'), '100g (Ref. Rótulo)', 100.0);
        """,
        # Açucares
        """
        INSERT IGNORE INTO tb_foods (name, food_group_id, default_portion_description, default_portion_grams) VALUES
        ('Doce de leite pastoso', (SELECT id from tb_food_groups WHERE name='Açúcares'), '1 colher de sopa (20g)', 20.0),
        ('Chocolate ao leite em barra', (SELECT id from tb_food_groups WHERE name='Açúcares'), '1 tablete pequeno (25g)', 25.0);
        """,

        # --- INFORMAÇÕES NUTRICIONAIS (tb_food_nutrients) ---
        # Mapeamento: 'Valor Energético' (kcal), 'Carboidrato Total' (carboidratos), 'Açúcares Totais' (açucares totais),
        # 'Proteína Total' (proteínas), 'Gorduras Totais' (gorduras totais)

        # Feijão carioca cozido (porção: 60g)
        """
        INSERT IGNORE INTO tb_food_nutrients (food_id, nutrient_id, amount_per_100_unit) VALUES
        ((SELECT id from tb_foods WHERE name='Feijão carioca cozido'), (SELECT id from tb_nutrients WHERE name='Valor Energético'), ROUND((164.0/60.0)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Feijão carioca cozido'), (SELECT id from tb_nutrients WHERE name='Carboidrato Total'), ROUND((17.0/60.0)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Feijão carioca cozido'), (SELECT id from tb_nutrients WHERE name='Açúcares Totais'), ROUND((2.6/60.0)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Feijão carioca cozido'), (SELECT id from tb_nutrients WHERE name='Proteína Total'), ROUND((11.0/60.0)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Feijão carioca cozido'), (SELECT id from tb_nutrients WHERE name='Gorduras Totais'), ROUND((1.3/60.0)*100, 1));
        """,
        # Arroz branco cozido (porção: 50g)
        """
        INSERT IGNORE INTO tb_food_nutrients (food_id, nutrient_id, amount_per_100_unit) VALUES
        ((SELECT id from tb_foods WHERE name='Arroz branco cozido'), (SELECT id from tb_nutrients WHERE name='Valor Energético'), ROUND((177.0/50.0)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Arroz branco cozido'), (SELECT id from tb_nutrients WHERE name='Carboidrato Total'), ROUND((39.0/50.0)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Arroz branco cozido'), (SELECT id from tb_nutrients WHERE name='Açúcares Totais'), ROUND((0.0/50.0)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Arroz branco cozido'), (SELECT id from tb_nutrients WHERE name='Proteína Total'), ROUND((3.9/50.0)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Arroz branco cozido'), (SELECT id from tb_nutrients WHERE name='Gorduras Totais'), ROUND((0.5/50.0)*100, 1));
        """,
        # Batata inglesa cozida (porção: 100g)
        """
        INSERT IGNORE INTO tb_food_nutrients (food_id, nutrient_id, amount_per_100_unit) VALUES
        ((SELECT id from tb_foods WHERE name='Batata inglesa cozida'), (SELECT id from tb_nutrients WHERE name='Valor Energético'), 51.0),
        ((SELECT id from tb_foods WHERE name='Batata inglesa cozida'), (SELECT id from tb_nutrients WHERE name='Carboidrato Total'), 10.8),
        ((SELECT id from tb_foods WHERE name='Batata inglesa cozida'), (SELECT id from tb_nutrients WHERE name='Açúcares Totais'), 0.0),
        ((SELECT id from tb_foods WHERE name='Batata inglesa cozida'), (SELECT id from tb_nutrients WHERE name='Proteína Total'), 1.3),
        ((SELECT id from tb_foods WHERE name='Batata inglesa cozida'), (SELECT id from tb_nutrients WHERE name='Gorduras Totais'), 0.5);
        """,
        # Batata doce cozida (porção: 100g)
        """
        INSERT IGNORE INTO tb_food_nutrients (food_id, nutrient_id, amount_per_100_unit) VALUES
        ((SELECT id from tb_foods WHERE name='Batata doce cozida'), (SELECT id from tb_nutrients WHERE name='Valor Energético'), 91.0),
        ((SELECT id from tb_foods WHERE name='Batata doce cozida'), (SELECT id from tb_nutrients WHERE name='Carboidrato Total'), 20.3),
        ((SELECT id from tb_foods WHERE name='Batata doce cozida'), (SELECT id from tb_nutrients WHERE name='Açúcares Totais'), 0.0),
        ((SELECT id from tb_foods WHERE name='Batata doce cozida'), (SELECT id from tb_nutrients WHERE name='Proteína Total'), 0.8),
        ((SELECT id from tb_foods WHERE name='Batata doce cozida'), (SELECT id from tb_nutrients WHERE name='Gorduras Totais'), 0.1);
        """,
        # Macarrão cozido (porção: 80g)
        """
        INSERT IGNORE INTO tb_food_nutrients (food_id, nutrient_id, amount_per_100_unit) VALUES
        ((SELECT id from tb_foods WHERE name='Macarrão cozido'), (SELECT id from tb_nutrients WHERE name='Valor Energético'), ROUND((288.0/80.0)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Macarrão cozido'), (SELECT id from tb_nutrients WHERE name='Carboidrato Total'), ROUND((59.0/80.0)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Macarrão cozido'), (SELECT id from tb_nutrients WHERE name='Açúcares Totais'), ROUND((2.5/80.0)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Macarrão cozido'), (SELECT id from tb_nutrients WHERE name='Proteína Total'), ROUND((10.0/80.0)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Macarrão cozido'), (SELECT id from tb_nutrients WHERE name='Gorduras Totais'), ROUND((1.0/80.0)*100, 1));
        """,
        # Pão francês (porção: 50g)
        """
        INSERT IGNORE INTO tb_food_nutrients (food_id, nutrient_id, amount_per_100_unit) VALUES
        ((SELECT id from tb_foods WHERE name='Pão francês'), (SELECT id from tb_nutrients WHERE name='Valor Energético'), ROUND((140.0/50.0)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Pão francês'), (SELECT id from tb_nutrients WHERE name='Carboidrato Total'), ROUND((30.0/50.0)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Pão francês'), (SELECT id from tb_nutrients WHERE name='Açúcares Totais'), ROUND((0.0/50.0)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Pão francês'), (SELECT id from tb_nutrients WHERE name='Proteína Total'), ROUND((4.0/50.0)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Pão francês'), (SELECT id from tb_nutrients WHERE name='Gorduras Totais'), ROUND((1.0/50.0)*100, 1));
        """,
        # Pão de forma tradicional (porção: 50g)
        """
        INSERT IGNORE INTO tb_food_nutrients (food_id, nutrient_id, amount_per_100_unit) VALUES
        ((SELECT id from tb_foods WHERE name='Pão de forma tradicional'), (SELECT id from tb_nutrients WHERE name='Valor Energético'), ROUND((127.0/50.0)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Pão de forma tradicional'), (SELECT id from tb_nutrients WHERE name='Carboidrato Total'), ROUND((25.0/50.0)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Pão de forma tradicional'), (SELECT id from tb_nutrients WHERE name='Açúcares Totais'), ROUND((2.4/50.0)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Pão de forma tradicional'), (SELECT id from tb_nutrients WHERE name='Proteína Total'), ROUND((4.2/50.0)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Pão de forma tradicional'), (SELECT id from tb_nutrients WHERE name='Gorduras Totais'), ROUND((1.3/50.0)*100, 1));
        """,
        # Goma de tapioca (porção: 100g)
        """
        INSERT IGNORE INTO tb_food_nutrients (food_id, nutrient_id, amount_per_100_unit) VALUES
        ((SELECT id from tb_foods WHERE name='Goma de tapioca'), (SELECT id from tb_nutrients WHERE name='Valor Energético'), 288.0),
        ((SELECT id from tb_foods WHERE name='Goma de tapioca'), (SELECT id from tb_nutrients WHERE name='Carboidrato Total'), 72.0),
        ((SELECT id from tb_foods WHERE name='Goma de tapioca'), (SELECT id from tb_nutrients WHERE name='Açúcares Totais'), 0.0),
        ((SELECT id from tb_foods WHERE name='Goma de tapioca'), (SELECT id from tb_nutrients WHERE name='Proteína Total'), 0.0),
        ((SELECT id from tb_foods WHERE name='Goma de tapioca'), (SELECT id from tb_nutrients WHERE name='Gorduras Totais'), 0.0);
        """,
        # Abóbora cozida (porção: 100g)
        """
        INSERT IGNORE INTO tb_food_nutrients (food_id, nutrient_id, amount_per_100_unit) VALUES
        ((SELECT id from tb_foods WHERE name='Abóbora cozida'), (SELECT id from tb_nutrients WHERE name='Valor Energético'), 26.0),
        ((SELECT id from tb_foods WHERE name='Abóbora cozida'), (SELECT id from tb_nutrients WHERE name='Carboidrato Total'), 6.5),
        ((SELECT id from tb_foods WHERE name='Abóbora cozida'), (SELECT id from tb_nutrients WHERE name='Açúcares Totais'), 2.7),
        ((SELECT id from tb_foods WHERE name='Abóbora cozida'), (SELECT id from tb_nutrients WHERE name='Proteína Total'), 1.0),
        ((SELECT id from tb_foods WHERE name='Abóbora cozida'), (SELECT id from tb_nutrients WHERE name='Gorduras Totais'), 0.1);
        """,
        # Berinjela cozida (porção: 100g)
        """
        INSERT IGNORE INTO tb_food_nutrients (food_id, nutrient_id, amount_per_100_unit) VALUES
        ((SELECT id from tb_foods WHERE name='Berinjela cozida'), (SELECT id from tb_nutrients WHERE name='Valor Energético'), 25.0),
        ((SELECT id from tb_foods WHERE name='Berinjela cozida'), (SELECT id from tb_nutrients WHERE name='Carboidrato Total'), 5.8),
        ((SELECT id from tb_foods WHERE name='Berinjela cozida'), (SELECT id from tb_nutrients WHERE name='Açúcares Totais'), 3.5),
        ((SELECT id from tb_foods WHERE name='Berinjela cozida'), (SELECT id from tb_nutrients WHERE name='Proteína Total'), 0.9),
        ((SELECT id from tb_foods WHERE name='Berinjela cozida'), (SELECT id from tb_nutrients WHERE name='Gorduras Totais'), 0.1);
        """,
        # Cenoura cozida (porção: 100g)
        """
        INSERT IGNORE INTO tb_food_nutrients (food_id, nutrient_id, amount_per_100_unit) VALUES
        ((SELECT id from tb_foods WHERE name='Cenoura cozida'), (SELECT id from tb_nutrients WHERE name='Valor Energético'), 41.0),
        ((SELECT id from tb_foods WHERE name='Cenoura cozida'), (SELECT id from tb_nutrients WHERE name='Carboidrato Total'), 9.5),
        ((SELECT id from tb_foods WHERE name='Cenoura cozida'), (SELECT id from tb_nutrients WHERE name='Açúcares Totais'), 4.7),
        ((SELECT id from tb_foods WHERE name='Cenoura cozida'), (SELECT id from tb_nutrients WHERE name='Proteína Total'), 0.93),
        ((SELECT id from tb_foods WHERE name='Cenoura cozida'), (SELECT id from tb_nutrients WHERE name='Gorduras Totais'), 0.23);
        """,
        # Beterraba cozida (porção: 100g)
        """
        INSERT IGNORE INTO tb_food_nutrients (food_id, nutrient_id, amount_per_100_unit) VALUES
        ((SELECT id from tb_foods WHERE name='Beterraba cozida'), (SELECT id from tb_nutrients WHERE name='Valor Energético'), 43.0),
        ((SELECT id from tb_foods WHERE name='Beterraba cozida'), (SELECT id from tb_nutrients WHERE name='Carboidrato Total'), 9.5),
        ((SELECT id from tb_foods WHERE name='Beterraba cozida'), (SELECT id from tb_nutrients WHERE name='Açúcares Totais'), 6.7),
        ((SELECT id from tb_foods WHERE name='Beterraba cozida'), (SELECT id from tb_nutrients WHERE name='Proteína Total'), 1.6),
        ((SELECT id from tb_foods WHERE name='Beterraba cozida'), (SELECT id from tb_nutrients WHERE name='Gorduras Totais'), 0.1);
        """,
        # Brócolis cozido (porção: 100g)
        """
        INSERT IGNORE INTO tb_food_nutrients (food_id, nutrient_id, amount_per_100_unit) VALUES
        ((SELECT id from tb_foods WHERE name='Brócolis cozido'), (SELECT id from tb_nutrients WHERE name='Valor Energético'), 34.0),
        ((SELECT id from tb_foods WHERE name='Brócolis cozido'), (SELECT id from tb_nutrients WHERE name='Carboidrato Total'), 6.6),
        ((SELECT id from tb_foods WHERE name='Brócolis cozido'), (SELECT id from tb_nutrients WHERE name='Açúcares Totais'), 1.0),
        ((SELECT id from tb_foods WHERE name='Brócolis cozido'), (SELECT id from tb_nutrients WHERE name='Proteína Total'), 2.8),
        ((SELECT id from tb_foods WHERE name='Brócolis cozido'), (SELECT id from tb_nutrients WHERE name='Gorduras Totais'), 0.3);
        """,
        # Melão (porção: 100g)
        """
        INSERT IGNORE INTO tb_food_nutrients (food_id, nutrient_id, amount_per_100_unit) VALUES
        ((SELECT id from tb_foods WHERE name='Melão'), (SELECT id from tb_nutrients WHERE name='Valor Energético'), 34.0),
        ((SELECT id from tb_foods WHERE name='Melão'), (SELECT id from tb_nutrients WHERE name='Carboidrato Total'), 8.1),
        ((SELECT id from tb_foods WHERE name='Melão'), (SELECT id from tb_nutrients WHERE name='Açúcares Totais'), 7.8),
        ((SELECT id from tb_foods WHERE name='Melão'), (SELECT id from tb_nutrients WHERE name='Proteína Total'), 0.5),
        ((SELECT id from tb_foods WHERE name='Melão'), (SELECT id from tb_nutrients WHERE name='Gorduras Totais'), 0.1);
        """,
        # Melancia (porção: 100g)
        """
        INSERT IGNORE INTO tb_food_nutrients (food_id, nutrient_id, amount_per_100_unit) VALUES
        ((SELECT id from tb_foods WHERE name='Melancia'), (SELECT id from tb_nutrients WHERE name='Valor Energético'), 32.0),
        ((SELECT id from tb_foods WHERE name='Melancia'), (SELECT id from tb_nutrients WHERE name='Carboidrato Total'), 7.5),
        ((SELECT id from tb_foods WHERE name='Melancia'), (SELECT id from tb_nutrients WHERE name='Açúcares Totais'), 6.2),
        ((SELECT id from tb_foods WHERE name='Melancia'), (SELECT id from tb_nutrients WHERE name='Proteína Total'), 0.6),
        ((SELECT id from tb_foods WHERE name='Melancia'), (SELECT id from tb_nutrients WHERE name='Gorduras Totais'), 0.1);
        """,
        # Morango (porção: 100g)
        """
        INSERT IGNORE INTO tb_food_nutrients (food_id, nutrient_id, amount_per_100_unit) VALUES
        ((SELECT id from tb_foods WHERE name='Morango'), (SELECT id from tb_nutrients WHERE name='Valor Energético'), 32.0),
        ((SELECT id from tb_foods WHERE name='Morango'), (SELECT id from tb_nutrients WHERE name='Carboidrato Total'), 7.6),
        ((SELECT id from tb_foods WHERE name='Morango'), (SELECT id from tb_nutrients WHERE name='Açúcares Totais'), 4.8),
        ((SELECT id from tb_foods WHERE name='Morango'), (SELECT id from tb_nutrients WHERE name='Proteína Total'), 0.6),
        ((SELECT id from tb_foods WHERE name='Morango'), (SELECT id from tb_nutrients WHERE name='Gorduras Totais'), 0.3);
        """,
        # Abacaxi (porção: 100g)
        """
        INSERT IGNORE INTO tb_food_nutrients (food_id, nutrient_id, amount_per_100_unit) VALUES
        ((SELECT id from tb_foods WHERE name='Abacaxi'), (SELECT id from tb_nutrients WHERE name='Valor Energético'), 50.0),
        ((SELECT id from tb_foods WHERE name='Abacaxi'), (SELECT id from tb_nutrients WHERE name='Carboidrato Total'), 13.1),
        ((SELECT id from tb_foods WHERE name='Abacaxi'), (SELECT id from tb_nutrients WHERE name='Açúcares Totais'), 9.85),
        ((SELECT id from tb_foods WHERE name='Abacaxi'), (SELECT id from tb_nutrients WHERE name='Proteína Total'), 0.5),
        ((SELECT id from tb_foods WHERE name='Abacaxi'), (SELECT id from tb_nutrients WHERE name='Gorduras Totais'), 0.1);
        """,
        # Kiwi (porção: 100g)
        """
        INSERT IGNORE INTO tb_food_nutrients (food_id, nutrient_id, amount_per_100_unit) VALUES
        ((SELECT id from tb_foods WHERE name='Kiwi'), (SELECT id from tb_nutrients WHERE name='Valor Energético'), 61.0),
        ((SELECT id from tb_foods WHERE name='Kiwi'), (SELECT id from tb_nutrients WHERE name='Carboidrato Total'), 14.6),
        ((SELECT id from tb_foods WHERE name='Kiwi'), (SELECT id from tb_nutrients WHERE name='Açúcares Totais'), 8.9),
        ((SELECT id from tb_foods WHERE name='Kiwi'), (SELECT id from tb_nutrients WHERE name='Proteína Total'), 1.1),
        ((SELECT id from tb_foods WHERE name='Kiwi'), (SELECT id from tb_nutrients WHERE name='Gorduras Totais'), 0.5);
        """,
        # Uva (porção: 100g)
        """
        INSERT IGNORE INTO tb_food_nutrients (food_id, nutrient_id, amount_per_100_unit) VALUES
        ((SELECT id from tb_foods WHERE name='Uva'), (SELECT id from tb_nutrients WHERE name='Valor Energético'), 67.0),
        ((SELECT id from tb_foods WHERE name='Uva'), (SELECT id from tb_nutrients WHERE name='Carboidrato Total'), 17.1),
        ((SELECT id from tb_foods WHERE name='Uva'), (SELECT id from tb_nutrients WHERE name='Açúcares Totais'), 15.4),
        ((SELECT id from tb_foods WHERE name='Uva'), (SELECT id from tb_nutrients WHERE name='Proteína Total'), 0.6),
        ((SELECT id from tb_foods WHERE name='Uva'), (SELECT id from tb_nutrients WHERE name='Gorduras Totais'), 0.1);
        """,
        # Ovos de galinha, cozidos (porção: 50g)
        """
        INSERT IGNORE INTO tb_food_nutrients (food_id, nutrient_id, amount_per_100_unit) VALUES
        ((SELECT id from tb_foods WHERE name='Ovos de galinha, cozidos'), (SELECT id from tb_nutrients WHERE name='Valor Energético'), ROUND((80.0/50.0)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Ovos de galinha, cozidos'), (SELECT id from tb_nutrients WHERE name='Carboidrato Total'), ROUND((1.0/50.0)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Ovos de galinha, cozidos'), (SELECT id from tb_nutrients WHERE name='Açúcares Totais'), ROUND((1.0/50.0)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Ovos de galinha, cozidos'), (SELECT id from tb_nutrients WHERE name='Proteína Total'), ROUND((7.0/50.0)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Ovos de galinha, cozidos'), (SELECT id from tb_nutrients WHERE name='Gorduras Totais'), ROUND((6.0/50.0)*100, 1));
        """,
        # Frango grelhado (peito) (porção: 100g)
        """
        INSERT IGNORE INTO tb_food_nutrients (food_id, nutrient_id, amount_per_100_unit) VALUES
        ((SELECT id from tb_foods WHERE name='Frango grelhado (peito)'), (SELECT id from tb_nutrients WHERE name='Valor Energético'), 165.0),
        ((SELECT id from tb_foods WHERE name='Frango grelhado (peito)'), (SELECT id from tb_nutrients WHERE name='Carboidrato Total'), 0.0),
        ((SELECT id from tb_foods WHERE name='Frango grelhado (peito)'), (SELECT id from tb_nutrients WHERE name='Açúcares Totais'), 0.0),
        ((SELECT id from tb_foods WHERE name='Frango grelhado (peito)'), (SELECT id from tb_nutrients WHERE name='Proteína Total'), 31.0),
        ((SELECT id from tb_foods WHERE name='Frango grelhado (peito)'), (SELECT id from tb_nutrients WHERE name='Gorduras Totais'), 3.6);
        """,
        # Patinho bovino, grelhado/moído (porção: 100g)
        """
        INSERT IGNORE INTO tb_food_nutrients (food_id, nutrient_id, amount_per_100_unit) VALUES
        ((SELECT id from tb_foods WHERE name='Patinho bovino, grelhado/moído'), (SELECT id from tb_nutrients WHERE name='Valor Energético'), 220.0),
        ((SELECT id from tb_foods WHERE name='Patinho bovino, grelhado/moído'), (SELECT id from tb_nutrients WHERE name='Carboidrato Total'), 3.0),
        ((SELECT id from tb_foods WHERE name='Patinho bovino, grelhado/moído'), (SELECT id from tb_nutrients WHERE name='Açúcares Totais'), 0.0),
        ((SELECT id from tb_foods WHERE name='Patinho bovino, grelhado/moído'), (SELECT id from tb_nutrients WHERE name='Proteína Total'), 36.0),
        ((SELECT id from tb_foods WHERE name='Patinho bovino, grelhado/moído'), (SELECT id from tb_nutrients WHERE name='Gorduras Totais'), 9.0);
        """,
        # Tilápia cozida (filé) (porção: 100g)
        """
        INSERT IGNORE INTO tb_food_nutrients (food_id, nutrient_id, amount_per_100_unit) VALUES
        ((SELECT id from tb_foods WHERE name='Tilápia cozida (filé)'), (SELECT id from tb_nutrients WHERE name='Valor Energético'), 130.0),
        ((SELECT id from tb_foods WHERE name='Tilápia cozida (filé)'), (SELECT id from tb_nutrients WHERE name='Carboidrato Total'), 1.0),
        ((SELECT id from tb_foods WHERE name='Tilápia cozida (filé)'), (SELECT id from tb_nutrients WHERE name='Açúcares Totais'), 0.0),
        ((SELECT id from tb_foods WHERE name='Tilápia cozida (filé)'), (SELECT id from tb_nutrients WHERE name='Proteína Total'), 26.0),
        ((SELECT id from tb_foods WHERE name='Tilápia cozida (filé)'), (SELECT id from tb_nutrients WHERE name='Gorduras Totais'), 3.0);
        """,
        # Whey Protein Concentrado (pó) (porção: 30g)
        """
        INSERT IGNORE INTO tb_food_nutrients (food_id, nutrient_id, amount_per_100_unit) VALUES
        ((SELECT id from tb_foods WHERE name='Whey Protein Concentrado (pó)'), (SELECT id from tb_nutrients WHERE name='Valor Energético'), ROUND((128.0/30.0)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Whey Protein Concentrado (pó)'), (SELECT id from tb_nutrients WHERE name='Carboidrato Total'), ROUND((4.2/30.0)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Whey Protein Concentrado (pó)'), (SELECT id from tb_nutrients WHERE name='Açúcares Totais'), ROUND((2.2/30.0)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Whey Protein Concentrado (pó)'), (SELECT id from tb_nutrients WHERE name='Proteína Total'), ROUND((22.0/30.0)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Whey Protein Concentrado (pó)'), (SELECT id from tb_nutrients WHERE name='Gorduras Totais'), ROUND((2.5/30.0)*100, 1));
        """,
        # Iogurte desnatado (Zero) (porção: 170g)
        """
        INSERT IGNORE INTO tb_food_nutrients (food_id, nutrient_id, amount_per_100_unit) VALUES
        ((SELECT id from tb_foods WHERE name='Iogurte desnatado (Zero)'), (SELECT id from tb_nutrients WHERE name='Valor Energético'), ROUND((44.0/170.0)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Iogurte desnatado (Zero)'), (SELECT id from tb_nutrients WHERE name='Carboidrato Total'), ROUND((6.1/170.0)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Iogurte desnatado (Zero)'), (SELECT id from tb_nutrients WHERE name='Açúcares Totais'), ROUND((6.1/170.0)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Iogurte desnatado (Zero)'), (SELECT id from tb_nutrients WHERE name='Proteína Total'), ROUND((4.8/170.0)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Iogurte desnatado (Zero)'), (SELECT id from tb_nutrients WHERE name='Gorduras Totais'), ROUND((0.0/170.0)*100, 1));
        """,
        # Requeijão cremoso light (porção informada 30g)
        """
        INSERT IGNORE INTO tb_food_nutrients (food_id, nutrient_id, amount_per_100_unit) VALUES
        ((SELECT id from tb_foods WHERE name='Requeijão cremoso light'), (SELECT id from tb_nutrients WHERE name='Valor Energético'), ROUND((64.0/30.0)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Requeijão cremoso light'), (SELECT id from tb_nutrients WHERE name='Carboidrato Total'), ROUND((3.8/30.0)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Requeijão cremoso light'), (SELECT id from tb_nutrients WHERE name='Açúcares Totais'), ROUND((0.8/30.0)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Requeijão cremoso light'), (SELECT id from tb_nutrients WHERE name='Proteína Total'), ROUND((7.9/30.0)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Requeijão cremoso light'), (SELECT id from tb_nutrients WHERE name='Gorduras Totais'), ROUND((9.0/30.0)*100, 1));
        """,
        # Margarina com sal (porção: 10g)
        """
        INSERT IGNORE INTO tb_food_nutrients (food_id, nutrient_id, amount_per_100_unit) VALUES
        ((SELECT id from tb_foods WHERE name='Margarina com sal'), (SELECT id from tb_nutrients WHERE name='Valor Energético'), ROUND((72.0/10.0)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Margarina com sal'), (SELECT id from tb_nutrients WHERE name='Carboidrato Total'), ROUND((0.0/10.0)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Margarina com sal'), (SELECT id from tb_nutrients WHERE name='Açúcares Totais'), ROUND((0.0/10.0)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Margarina com sal'), (SELECT id from tb_nutrients WHERE name='Proteína Total'), ROUND((0.0/10.0)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Margarina com sal'), (SELECT id from tb_nutrients WHERE name='Gorduras Totais'), ROUND((8.0/10.0)*100, 1));
        """,
        # Azeite de oliva extra virgem (porção: 13ml = 11.96g)
        """
        INSERT IGNORE INTO tb_food_nutrients (food_id, nutrient_id, amount_per_100_unit) VALUES
        ((SELECT id from tb_foods WHERE name='Azeite de oliva extra virgem'), (SELECT id from tb_nutrients WHERE name='Valor Energético'), ROUND((107.0/11.96)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Azeite de oliva extra virgem'), (SELECT id from tb_nutrients WHERE name='Carboidrato Total'), ROUND((0.0/11.96)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Azeite de oliva extra virgem'), (SELECT id from tb_nutrients WHERE name='Açúcares Totais'), ROUND((0.0/11.96)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Azeite de oliva extra virgem'), (SELECT id from tb_nutrients WHERE name='Proteína Total'), ROUND((0.0/11.96)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Azeite de oliva extra virgem'), (SELECT id from tb_nutrients WHERE name='Gorduras Totais'), ROUND((12.0/11.96)*100, 1));
        """,
        # Pasta de Amendoim integral (porção: 15g)
        """
        INSERT IGNORE INTO tb_food_nutrients (food_id, nutrient_id, amount_per_100_unit) VALUES
        ((SELECT id from tb_foods WHERE name='Pasta de Amendoim integral'), (SELECT id from tb_nutrients WHERE name='Valor Energético'), ROUND((88.0/15.0)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Pasta de Amendoim integral'), (SELECT id from tb_nutrients WHERE name='Carboidrato Total'), ROUND((3.0/15.0)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Pasta de Amendoim integral'), (SELECT id from tb_nutrients WHERE name='Açúcares Totais'), ROUND((0.0/15.0)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Pasta de Amendoim integral'), (SELECT id from tb_nutrients WHERE name='Proteína Total'), ROUND((4.1/15.0)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Pasta de Amendoim integral'), (SELECT id from tb_nutrients WHERE name='Gorduras Totais'), ROUND((6.6/15.0)*100, 1));
        """,
        # Castanha do Pará (porção: 100g)
        """
        INSERT IGNORE INTO tb_food_nutrients (food_id, nutrient_id, amount_per_100_unit) VALUES
        ((SELECT id from tb_foods WHERE name='Castanha do Pará'), (SELECT id from tb_nutrients WHERE name='Valor Energético'), 656.0),
        ((SELECT id from tb_foods WHERE name='Castanha do Pará'), (SELECT id from tb_nutrients WHERE name='Carboidrato Total'), 11.7),
        ((SELECT id from tb_foods WHERE name='Castanha do Pará'), (SELECT id from tb_nutrients WHERE name='Açúcares Totais'), 2.3),
        ((SELECT id from tb_foods WHERE name='Castanha do Pará'), (SELECT id from tb_nutrients WHERE name='Proteína Total'), 14.3),
        ((SELECT id from tb_foods WHERE name='Castanha do Pará'), (SELECT id from tb_nutrients WHERE name='Gorduras Totais'), 66.4);
        """,
        # Doce de leite pastoso (porção: 20g)
        """
        INSERT IGNORE INTO tb_food_nutrients (food_id, nutrient_id, amount_per_100_unit) VALUES
        ((SELECT id from tb_foods WHERE name='Doce de leite pastoso'), (SELECT id from tb_nutrients WHERE name='Valor Energético'), ROUND((70.0/20.0)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Doce de leite pastoso'), (SELECT id from tb_nutrients WHERE name='Carboidrato Total'), ROUND((14.0/20.0)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Doce de leite pastoso'), (SELECT id from tb_nutrients WHERE name='Açúcares Totais'), ROUND((14.0/20.0)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Doce de leite pastoso'), (SELECT id from tb_nutrients WHERE name='Proteína Total'), ROUND((1.9/20.0)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Doce de leite pastoso'), (SELECT id from tb_nutrients WHERE name='Gorduras Totais'), ROUND((7.6/20.0)*100, 1));
        """,
        # Chocolate ao leite em barra (porção: 25g)
        """
        INSERT IGNORE INTO tb_food_nutrients (food_id, nutrient_id, amount_per_100_unit) VALUES
        ((SELECT id from tb_foods WHERE name='Chocolate ao leite em barra'), (SELECT id from tb_nutrients WHERE name='Valor Energético'), ROUND((135.0/25.0)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Chocolate ao leite em barra'), (SELECT id from tb_nutrients WHERE name='Carboidrato Total'), ROUND((15.0/25.0)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Chocolate ao leite em barra'), (SELECT id from tb_nutrients WHERE name='Açúcares Totais'), ROUND((14.0/25.0)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Chocolate ao leite em barra'), (SELECT id from tb_nutrients WHERE name='Proteína Total'), ROUND((1.3/25.0)*100, 1)),
        ((SELECT id from tb_foods WHERE name='Chocolate ao leite em barra'), (SELECT id from tb_nutrients WHERE name='Gorduras Totais'), ROUND((1.7/25.0)*100, 1));
        """
    ]

    try:
        cursor = cnxn.cursor()
        for command_block_index, command_block in enumerate(insert_commands):
            try:
                cursor.execute(command_block)
                print(f"Bloco de comando {command_block_index + 1} executado.")
            except mysql.connector.Error as e:
                if e.errno == 1062: # ER_DUP_ENTRY
                    print(
                        f"Dado inicial já existe (ignorado) no bloco {command_block_index + 1}: {command_block.strip()[:70]}...")
                else:
                    print(
                        f"Erro ao executar comando/bloco {command_block_index + 1}: {command_block.strip()[:70]}... \nERRO: {e}")
        cnxn.commit()
        print("Dados iniciais (incluindo alimentos e seus nutrientes) verificados/inseridos com sucesso.")

    except mysql.connector.Error as e:
        print(f"Erro geral ao inserir dados iniciais: {e}")
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()


def setup_database():

    print("Iniciando configuração do banco de dados...")
    connection = connect_database()
    if connection:
        create_tables(connection)
        insert_initial_data(connection)
        connection.close()
        print("Configuração do banco de dados concluída.")
    else:
        print("Não foi possível configurar o banco de dados devido a falha na conexão inicial.")


if __name__ == "__main__":

    # Executar a configuração do banco de dados
    setup_database()