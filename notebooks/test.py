system_message = """
Usando los siguientes datos para la Compañía NU MX, crea un mensaje conciso dirigido a un empleado específico, resaltando áreas clave que requieren atención basadas en el análisis de datos. Los datos muestran disminuciones significativas en varios KPIs comparados con períodos anteriores. El mensaje debe ser breve, incluir ejemplos específicos de disminuciones en porcentajes, sugerir el impacto potencial de estas disminuciones, y concluir con una llamada a la acción para revisar el dashboard para más detalles. Mantén un tono directo, alentador y profesional. El mensaje debe mostrar numeros para cada alerta que se muestre


>>> Ejemplo de mensaje:
Compañía: NU MX
    Canal: INBOUND
        KPI: BARRIDO
            :small_red_triangle_down: Actual: 0.07% | Debajo por -0.09% contra Febrero (0.16%) y  -0.1% contra Enero (0.17%)
        KPI: COMPROMISO
            :small_red_triangle_down: Actual: 0.03% | Debajo por -0.04% contra Febrero (0.07%) y  -0.03% contra Enero (0.06%)
    Canal: TOTAL
        KPI: COMPROMISO
            :small_red_triangle_down: Actual: 0.87% | Debajo por -0.45% contra Enero (1.32%)
    Canal: EMAIL
        KPI: BARRIDO
            :small_red_triangle_down: Actual: 51.03% | Debajo por -30.87% contra Febrero (81.9%) y  -38.51% contra Enero (89.54%)
    Canal: HUMAN
        KPI: BARRIDO
            :small_red_triangle_down: Actual: 27.3% | Debajo por -31.25% contra Febrero (58.55%) y  -28.8% contra Enero (56.1%)
        KPI: COMPROMISO
            :small_red_triangle_down: Actual: 0.79% | Debajo por -0.43% contra Enero (1.22%)
    Canal: IVR
        KPI: BARRIDO
            :small_red_triangle_down: Actual: 10.16% | Debajo por -47.51% contra Febrero (57.67%) y  -46.25% contra Enero (56.41%)
        KPI: CONTACTO_DIRECTO
            :small_red_triangle_down: Actual: 0.04% | Debajo por -0.26% contra Febrero (0.3%) y  -0.25% contra Enero (0.29%)
    Canal: SMS
        KPI: CONTACTO
            :small_red_triangle_down: Actual: 0.04% | Debajo por -0.07% contra Enero (0.11%)
    Canal: WHATSAPP
        KPI: BARRIDO
            :small_red_triangle_down: Actual: 0.06% | Debajo por -0.03% contra Febrero (0.09%) y  -0.03% contra Enero (0.09%)
        KPI: COMPROMISO
            :small_red_triangle_down: Actual: 0.02% | Debajo por -0.01% contra Febrero (0.03%) y  -0.01% contra Enero (0.03%)

>>> Ejemplo de resultado esperado: 

"**Compañía: NU MX**

¡Buen día!

Al revisar el dashboard de NU MX, destacan algunas áreas para enfocarnos hoy:

- **INBOUND**: Necesitamos mejorar en BARRIDO y COMPROMISO, con caídas del 0.09% y 0.04% respecto a febrero.
- **TOTAL / COMPROMISO**: Estamos a 0.87%, lejos del 1.32% de enero. Requiere atención.
- **Canales EMAIL y HUMAN**: Grandes caídas en BARRIDO desde febrero, de un 38% y 28% respectivamente. Vale la pena investigar.
- **IVR**: Alerta en BARRIDO y CONTACTO_DIRECTO, con caídas significativas.
- **SMS y WHATSAPP**: Pequeñas caídas en CONTACTO, BARRIDO y COMPROMISO. Revisar ajustes posibles.

Por favor, echa un vistazo a estos puntos hoy. Cualquier duda, aquí estoy.

¡Gracias! 🚀"

"""

portfolio_data = """
Compañía: NU MX
    Canal: INBOUND
        KPI: BARRIDO
            :small_red_triangle_down: Actual: 0.07% | Debajo por -0.09% contra Febrero (0.16%) y  -0.1% contra Enero (0.17%)
        KPI: COMPROMISO
            :small_red_triangle_down: Actual: 0.03% | Debajo por -0.04% contra Febrero (0.07%) y  -0.03% contra Enero (0.06%)
    Canal: TOTAL
        KPI: COMPROMISO
            :small_red_triangle_down: Actual: 0.87% | Debajo por -0.45% contra Enero (1.32%)
    Canal: EMAIL
        KPI: BARRIDO
            :small_red_triangle_down: Actual: 51.03% | Debajo por -30.87% contra Febrero (81.9%) y  -38.51% contra Enero (89.54%)
    Canal: HUMAN
        KPI: BARRIDO
            :small_red_triangle_down: Actual: 27.3% | Debajo por -31.25% contra Febrero (58.55%) y  -28.8% contra Enero (56.1%)
        KPI: COMPROMISO
            :small_red_triangle_down: Actual: 0.79% | Debajo por -0.43% contra Enero (1.22%)
    Canal: IVR
        KPI: BARRIDO
            :small_red_triangle_down: Actual: 10.16% | Debajo por -47.51% contra Febrero (57.67%) y  -46.25% contra Enero (56.41%)
        KPI: CONTACTO_DIRECTO
            :small_red_triangle_down: Actual: 0.04% | Debajo por -0.26% contra Febrero (0.3%) y  -0.25% contra Enero (0.29%)
    Canal: SMS
        KPI: CONTACTO
            :small_red_triangle_down: Actual: 0.04% | Debajo por -0.07% contra Enero (0.11%)
    Canal: WHATSAPP
        KPI: BARRIDO
            :small_red_triangle_down: Actual: 0.06% | Debajo por -0.03% contra Febrero (0.09%) y  -0.03% contra Enero (0.09%)
        KPI: COMPROMISO
            :small_red_triangle_down: Actual: 0.02% | Debajo por -0.01% contra Febrero (0.03%) y  -0.01% contra Enero (0.03%)

"""
