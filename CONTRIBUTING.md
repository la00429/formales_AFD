# Contribuir al AFD Simulator

## 🤝 Cómo Contribuir

¡Las contribuciones son bienvenidas! Este proyecto está diseñado para ser educativo y extensible.

### Estructura del Proyecto

```
afd_simulator/
├── core/           # Lógica principal del AFD
├── ui/            # Interfaz de consola
├── gui/           # Interfaz gráfica
├── utils/         # Utilidades y validadores
├── examples/      # Factory de AFD comunes
├── data/          # Ejemplos en JSON
└── entry_points/  # Puntos de entrada
```

### Tipos de Contribuciones

1. **Nuevos Patrones de AFD**: Agregar al factory nuevos AFD comunes
2. **Mejoras de GUI**: Mejorar la interfaz gráfica
3. **Algoritmos**: Optimizar generación de cadenas o validación
4. **Documentación**: Mejorar ejemplos y guías
5. **Testing**: Agregar casos de prueba

### Estilo de Código

- **Idioma**: Código en inglés, comentarios en español
- **Formato**: PEP 8 con líneas de máximo 100 caracteres
- **Docstrings**: Formato Google style
- **Type hints**: Usar typing para mejor documentación

### Commits

Usar formato conventional commits:
- `feat:` para nuevas características
- `fix:` para corrección de bugs
- `docs:` para documentación
- `refactor:` para refactoring
- `test:` para testing

### Testing

Probar en:
- Consola: `python main.py --demo`
- GUI: `python main.py --gui`
- Módulo: `python -m afd_simulator --demo`

## 📧 Contacto

Para preguntas o sugerencias, crear un issue en el repositorio.
