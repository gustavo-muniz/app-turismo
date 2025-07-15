import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# --- Dados Fictícios (Simulados) ---
# Usuários para simular login
USUARIOS = {
    "turista@exemplo.com": "12345",
    "admin@exemplo.com": "admin123"
}

# Pontos Turísticos de Natal
PONTOS_TURISTICOS = {
    "Ponta Negra": {
        "descricao": "Famosa praia urbana com o Morro do Careca, um dos cartões-postais mais icônicos de Natal. Ideal para banho, esportes na areia e apreciação do pôr do sol.",
        "latitude": -5.8856,
        "longitude": -35.1843,
        "imagem": "https://vidasemparedes.com.br/wp-content/uploads/2020/03/natal-rn-vidasemparedes-1.jpg",
        "historia": "Ponta Negra era uma antiga vila de pescadores que se transformou em um dos principais destinos turísticos do Nordeste brasileiro. O Morro do Careca, uma grande duna, é sua característica mais marcante."
    },
    "Parque das Dunas": {
        "descricao": "Maior parque urbano sobre dunas do Brasil, com extensa área de Mata Atlântica preservada, trilhas ecológicas e mirantes.",
        "latitude": -5.8239,
        "longitude": -35.2016,
        "imagem": "https://coralplaza.com.br/wp-content/uploads/2020/06/204705-parque-das-dunas-conheca-a-sua-historia-e-as-suas-belezas.jpg",
        "historia": "Criado em 1977, o Parque Estadual Dunas de Natal 'Jornalista Luiz Maria Alves' é uma unidade de conservação fundamental para o ecossistema local e para o lazer da população."
    },
    "Forte dos Reis Magos": {
        "descricao": "Fortaleza histórica em forma de estrela, construída pelos portugueses na foz do Rio Potengi, marco inicial da cidade de Natal.",
        "latitude": -5.7629,
        "longitude": -35.1927,
        "imagem": "https://s2-g1.glbimg.com/bBVZJdVdrjt7i6sd3Prvmi6qLYU=/0x0:1280x720/984x0/smart/filters:strip_icc()/i.s3.glbimg.com/v1/AUTH_59edd422c0c84a879bd37670ae4f538a/internal_photos/bs/2021/7/A/pjh8pYQcq7yt55bnjBzA/sandro-menezes5.jpg",
        "historia": "Sua construção iniciou em 1598, no dia de Reis, dando nome ao forte e, posteriormente, à cidade de Natal. Foi fundamental na defesa da costa contra invasões holandesas."
    },
    "Centro de Turismo": {
        "descricao": "Antiga prisão que hoje abriga lojas de artesanato local, com vista panorâmica para o Rio Potengi.",
        "latitude": -5.7744,
        "longitude": -35.2013,
        "imagem": "https://marazulreceptivo.com.br/wp-content/uploads/2024/07/Centro-de-turismo-em-Natal-RN.png",
        "historia": "O prédio já foi a antiga Casa de Detenção de Natal. Hoje, é um ponto vibrante do artesanato e da cultura potiguar, famoso pelo forró com o 'Forró com Turista'."
    }
}

# Rotas (apenas nomes para simular, detalhes viriam de lista de pontos)
ROTAS_POPULARES = [
    "Rota das Praias do Sul",
    "História e Cultura de Natal",
    "Belezas Naturais Urbanas"
]

ROTA_USUARIO_EXEMPLO = [
    "Ponta Negra",
    "Forte dos Reis Magos"
]


# --- Variável de Estado para simular login ---
if 'logado' not in st.session_state:
    st.session_state['logado'] = False
    st.session_state['usuario'] = None
    st.session_state['role'] = None # 'turista' ou 'admin'

if 'current_page' not in st.session_state:
    st.session_state['current_page'] = "login" # Página inicial

# --- Funções para as "Páginas" ---

def pagina_login():
    st.title("Bem-vindo de volta")
    st.write("---")

    with st.form("login_form"):
        email = st.text_input("Email:", placeholder="seu.email@exemplo.com")
        senha = st.text_input("Senha:", type="password", placeholder="Sua senha")
        submitted = st.form_submit_button("Entrar")

        if submitted:
            if email in USUARIOS and USUARIOS[email] == senha:
                st.session_state['logado'] = True
                st.session_state['usuario'] = email
                if email == "admin@exemplo.com":
                    st.session_state['role'] = 'admin'
                    st.session_state['current_page'] = "gerenciar_pontos" # Redireciona admin para sua página
                else:
                    st.session_state['role'] = 'turista'
                    st.session_state['current_page'] = "mapa" # Redireciona turista para o mapa
                st.rerun() # Atualiza a página para mostrar o conteúdo correto
            else:
                st.error("Email ou senha incorretos.")

def pagina_mapa_natal():
    st.subheader("Mapa de Natal")
    st.write("Explore os pontos turísticos de Natal/RN no mapa.")

    # Centra o mapa em Natal
    m = folium.Map(location=[-5.795, -35.209], zoom_start=12)

    for nome, dados in PONTOS_TURISTICOS.items():
        folium.Marker(
            location=[dados["latitude"], dados["longitude"]],
            popup=f"<b>{nome}</b><br>{dados['descricao']}",
            tooltip=nome
        ).add_to(m)

    folium_static(m, width=700, height=500) # Ajuste a largura e altura conforme necessário

def pagina_explore_natal(ponto_selecionado_externo=None):
    st.subheader("Explore Natal")

    pontos_nomes = list(PONTOS_TURISTICOS.keys())
    if ponto_selecionado_externo and ponto_selecionado_externo in pontos_nomes:
        idx_selecionado = pontos_nomes.index(ponto_selecionado_externo)
    else:
        idx_selecionado = 0 # Default para o primeiro item

    ponto_selecionado = st.selectbox(
        "Selecione um ponto turístico para ver detalhes:",
        pontos_nomes,
        index=idx_selecionado,
        key="explore_select_ponto"
    )

    if ponto_selecionado:
        dados = PONTOS_TURISTICOS[ponto_selecionado]
        col1, col2 = st.columns([1, 2])
        with col1:
            if dados.get("imagem"):
                st.image(dados["imagem"], caption=ponto_selecionado, use_container_width =True)
            else:
                st.image("https://via.placeholder.com/300x200?text=Imagem+N%C3%A3o+Dispon%C3%ADvel", caption="Imagem não disponível")

        with col2:
            st.title(ponto_selecionado) # Título maior para o nome do ponto
            st.header("About")
            st.write(dados["descricao"])
            st.header("History")
            st.write(dados["historia"])

        st.markdown("---")
        st.subheader("Avaliar este Ponto")
        nota = st.slider("Sua nota (1 a 5):", 1, 5, 3, key=f"nota_{ponto_selecionado}")
        comentario = st.text_area("Seu comentário:", placeholder="Compartilhe sua experiência aqui...", key=f"comentario_{ponto_selecionado}")
        if st.button(f"Enviar Avaliação para {ponto_selecionado}", key=f"btn_avaliacao_{ponto_selecionado}"):
            st.success(f"Sua avaliação para '{ponto_selecionado}' (Nota: {nota}, Comentário: '{comentario}') foi registrada! (Simulado)")

def pagina_minhas_rotas():
    st.subheader("Minhas Rotas")
    st.write("Crie e gerencie suas rotas e pontos favoritos.")

    st.header("Minhas Rotas Criadas")
    if ROTA_USUARIO_EXEMPLO:
        for i, ponto_nome in enumerate(ROTA_USUARIO_EXEMPLO):
            dados = PONTOS_TURISTICOS.get(ponto_nome)
            if dados:
                col1, col2 = st.columns([1, 3])
                with col1:
                    if dados.get("imagem"):
                        st.image(dados["imagem"], width=100)
                    else:
                        st.image("https://via.placeholder.com/100x70?text=Sem+Foto")
                with col2:
                    st.write(f"**{ponto_nome}**")
                    st.write(dados["descricao"][:70] + "..." if len(dados["descricao"]) > 70 else dados["descricao"])
                    # Botões de ação, se houver
                    # st.button(f"Remover da Rota {i}", key=f"remove_rota_{i}")
            else:
                st.warning(f"Ponto '{ponto_nome}' não encontrado.")
    else:
        st.info("Você ainda não adicionou pontos à sua rota.")

    st.markdown("---")
    st.header("Adicionar Ponto à Rota")
    ponto_para_adicionar = st.selectbox(
        "Selecione um ponto para adicionar à sua rota:",
        ["Selecione"] + [p for p in list(PONTOS_TURISTICOS.keys()) if p not in ROTA_USUARIO_EXEMPLO],
        key="add_ponto_rota"
    )
    if st.button("Adicionar à Rota"):
        if ponto_para_adicionar != "Selecione":
            ROTA_USUARIO_EXEMPLO.append(ponto_para_adicionar)
            st.success(f"'{ponto_para_adicionar}' adicionado à sua rota! (Simulado)")
            st.rerun() # Atualiza a página para mostrar o novo item

def pagina_rotas_populares():
    st.subheader("Rotas Populares")
    st.write("Descubra rotas pré-definidas e inspire-se para sua viagem.")

    for rota in ROTAS_POPULARES:
        st.markdown(f"### {rota}")
        # Aqui você listaria os pontos da rota
        st.write("*(Esta rota incluiria vários pontos turísticos, como...)*")
        st.markdown("---")

    st.header("Crie Sua Própria Rota")
    nova_rota_nome = st.text_input("Nome da Nova Rota:")
    pontos_disponiveis = list(PONTOS_TURISTICOS.keys())
    pontos_selecionados = st.multiselect(
        "Selecione os pontos para sua rota:",
        pontos_disponiveis,
        key="criar_rota_pontos"
    )

    if st.button("Criar Rota"):
        if nova_rota_nome and pontos_selecionados:
            st.success(f"Rota '{nova_rota_nome}' criada com sucesso com {len(pontos_selecionados)} pontos! (Simulado)")
            st.write("Pontos na rota:", ", ".join(pontos_selecionados))
        else:
            st.warning("Por favor, preencha o nome da rota e selecione pelo menos um ponto.")

def pagina_gerenciar_pontos():
    st.subheader("Gerenciar Pontos Turísticos (Admin)")
    st.write("Aqui você pode cadastrar, editar e remover pontos turísticos.")

    st.markdown("---")
    st.subheader("Cadastrar Novo Ponto Turístico")
    with st.form("form_novo_ponto_admin"):
        novo_nome = st.text_input("Nome do Ponto Turístico:", key="admin_nome")
        nova_descricao = st.text_area("Descrição:", key="admin_descricao")
        nova_historia = st.text_area("História:", key="admin_historia")
        nova_latitude = st.number_input("Latitude:", format="%.4f", key="admin_lat")
        nova_longitude = st.number_input("Longitude:", format="%.4f", key="admin_lon")
        nova_imagem_url = st.text_input("URL da Imagem (opcional):", placeholder="Ex: https://exemplo.com/imagem.jpg", key="admin_img_url")

        submitted = st.form_submit_button("Cadastrar Ponto")
        if submitted:
            if novo_nome and nova_descricao and nova_latitude and nova_longitude:
                # Adiciona o novo ponto aos dados fictícios (temporariamente)
                PONTOS_TURISTICOS[novo_nome] = {
                    "descricao": nova_descricao,
                    "historia": nova_historia,
                    "latitude": nova_latitude,
                    "longitude": nova_longitude,
                    "imagem": nova_imagem_url if nova_imagem_url else None
                }
                st.success(f"Ponto turístico '{novo_nome}' cadastrado com sucesso! (Simulado)")
                st.rerun() # Atualiza a página para que o novo ponto apareça nas listas
            else:
                st.error("Por favor, preencha todos os campos obrigatórios (nome, descrição, lat, lon).")

    st.markdown("---")
    st.subheader("Pontos Turísticos Cadastrados")
    pontos_df = pd.DataFrame([
        {"Nome": nome, "Descrição": dados["descricao"][:50] + "..." if len(dados["descricao"]) > 50 else dados["descricao"], "Lat": dados["latitude"], "Lon": dados["longitude"]}
        for nome, dados in PONTOS_TURISTICOS.items()
    ])
    if not pontos_df.empty:
        st.dataframe(pontos_df, hide_index=True)
    else:
        st.info("Nenhum ponto turístico cadastrado ainda.")

    st.markdown("---")
    st.subheader("Editar/Remover Ponto Turístico (Simulação)")
    ponto_para_gerenciar = st.selectbox(
        "Selecione um ponto para editar ou remover:",
        ["Selecione"] + list(PONTOS_TURISTICOS.keys()),
        key="gerenciar_ponto_select"
    )

    if ponto_para_gerenciar != "Selecione":
        st.write(f"Detalhes de '{ponto_para_gerenciar}':")
        dados_gerenciar = PONTOS_TURISTICOS[ponto_para_gerenciar]
        st.json(dados_gerenciar) # Exibe os dados em formato JSON para simplicidade

        col_gerenciar_btn1, col_gerenciar_btn2 = st.columns(2)
        with col_gerenciar_btn1:
            if st.button(f"Simular Edição de '{ponto_para_gerenciar}'"):
                st.info(f"Simulando edição de '{ponto_para_gerenciar}'. (Formulário de edição apareceria aqui)")
        with col_gerenciar_btn2:
            if st.button(f"Simular Remoção de '{ponto_para_gerenciar}'"):
                st.warning(f"Simulando remoção de '{ponto_para_gerenciar}'. (Confirmação apareceria aqui)")
                # Em um sistema real, você removeria o item do dicionário ou DB.
                # Para protótipo, não removeremos para manter a base de dados simulada.


# --- Lógica Principal do Aplicativo ---
def main_app():
    st.set_page_config(page_title="Natal Turismo App (Protótipo)", layout="wide", initial_sidebar_state="expanded")

    if not st.session_state['logado']:
        pagina_login()
    else:
        st.sidebar.title(f"Bem-vindo, {st.session_state['usuario']}")
        
        # Logout
        if st.sidebar.button("Sair"):
            st.session_state['logado'] = False
            st.session_state['usuario'] = None
            st.session_state['role'] = None
            st.session_state['current_page'] = "login"
            st.rerun()

        # Menu de Navegação na barra lateral
        if st.session_state['role'] == 'admin':
            opcoes_menu = {
                "Gerenciar Pontos": "gerenciar_pontos",
                "Mapa": "mapa",
                "Explore": "explore_natal"
            }
        else: # Turista
            opcoes_menu = {
                "Mapa": "mapa",
                "Explore": "explore_natal",
                "Minhas Rotas": "minhas_rotas",
                "Rotas Populares": "rotas_populares"
            }
        
        # Navegação com base na session_state['current_page']
        # Usamos um radio button com chave, e o valor default é a página atual
        page_names = list(opcoes_menu.keys())
        default_index = 0
        for i, name in enumerate(page_names):
            if opcoes_menu[name] == st.session_state['current_page']:
                default_index = i
                break

        st.session_state['current_page'] = st.sidebar.radio(
            "Navegação:",
            options=page_names,
            index=default_index,
            key="main_menu_radio"
        )
        # Atualiza a página atual com o valor selecionado
        st.session_state['current_page'] = opcoes_menu[st.session_state['current_page']]

        # Renderiza a página selecionada
        if st.session_state['current_page'] == "mapa":
            pagina_mapa_natal()
        elif st.session_state['current_page'] == "explore_natal":
            pagina_explore_natal()
        elif st.session_state['current_page'] == "minhas_rotas":
            if st.session_state['role'] == 'turista':
                pagina_minhas_rotas()
            else:
                st.warning("Acesso negado. Esta página é apenas para turistas.")
        elif st.session_state['current_page'] == "rotas_populares":
            if st.session_state['role'] == 'turista':
                pagina_rotas_populares()
            else:
                st.warning("Acesso negado. Esta página é apenas para turistas.")
        elif st.session_state['current_page'] == "gerenciar_pontos":
            if st.session_state['role'] == 'admin':
                pagina_gerenciar_pontos()
            else:
                st.warning("Acesso negado. Esta página é apenas para administradores.")


if __name__ == "__main__":
    main_app()