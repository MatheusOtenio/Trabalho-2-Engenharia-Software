def mostrar_dashboard(perfil):
    print(f"\n📊 DASHBOARD DE {perfil.nome.upper()}")
    print(f"🆔 RA: {perfil.ra}")
    print(f"📧 Email: {perfil.email}")
    print(f"📘 Matérias de interesse: {', '.join(perfil.materias_interesse) if perfil.materias_interesse else 'Nenhuma'}")
    print(f"🧩 Grupos participados: {perfil.grupos_participados}")
    print("-" * 40)
