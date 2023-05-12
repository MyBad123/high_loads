from django.db import models
from urllib.parse import unquote
from datetime import date
from jinja2 import Template


DESCRIPTIONS = {
    'book': {
        'data': "{% if responsibility %} ; {{ responsibility }}{% endif %}{% if edit_info %}. – {{ edit_info }}{% endif %}{% if par_edit_info %} = {{ par_edit_info }}{% endif %}{% if liability %} / {{ liability }}{% endif %}. – {{ place }} : {{ publishing }}, {{ year }}{% if place_of_distribution %} ; {{ place_of_distribution }}{% endif %}{% if organization_of_distribution %} : {{ organization_of_distribution }} [распространитель],{% endif %}{% if distribution_date %} {{ distribution_date }}{% endif %}{% if manufacture %} ({{ manufacture }}){% endif %}. – {{ pages }}{% if unnumbered_pages %}, [{{ unnumbered_pages }}]{% endif %} с.{% if illustrations %}, {{ illustrations }}{% endif %}{% if physical_characteristics %} : {{ physical_characteristics }}{% endif %}{% if size %} ; {{ size }} см{% endif %}{% if accompanying %} + {{ accompanying }}{% endif %}{% if main_title %} ({{ main_title }}{% if parallel_series_title %} = {{ parallel_series_title }}{% endif %}{% if series_title_information %} : {{ series_title_information }}{% endif %}{% if responsibility_info %} / {{ responsibility_info }}{% endif %}{% if number %}, {{ number }}{% endif %}{% if serial_number %} ; {{ serial_number }}{% endif %}{% if sub_main_title %}. {{ sub_main_title }}{% endif %}{% if sub_parallel_series_title %} = {{ sub_parallel_series_title }}{% endif %}{% if sub_series_title_information %} : {{ sub_series_title_information }}{% endif %}{% if sub_responsibility_info %} / {{ sub_responsibility_info }}{% endif %}{% if sub_number %}, {{ sub_number }}{% endif %}{% if sub_serial_number %} ; {{ sub_serial_number }}{% endif %}){% endif %}{% if notes %}. – {{ notes }}{% endif %}{% if general_notes %}. – {{ general_notes }}{% endif %}{% if isbn %} – ISBN {{ isbn }}{% endif %}{% if additional_information %} ({{ additional_information }}){% endif %}{% if fingerprint %}. – Фингерпринт: {{ fingerprint }}{% endif %}{% if availability %} : {{ availability }}{% endif %}{% if content %}. – {{ content }}{% endif %}{% if content_type %} ({{ content_type }}){% endif %}{% if access_means %} : {{ access_means }}{% endif %}",
        'authors': '''
            {% if fourth_surname or fourth_initials %}
                {{ title }}{% if parallel %} = {{ parallel }}{% endif %}{% if type_doc %} : {{ type_doc }}{% endif %}{% if explanations %} : [{{ explanations }}]{% endif %} / {{ initials }} {{ surname }}, {{ second_initials_3 }} {{ second_surname_3 }}, {{ third_initials_2 }} {{ third_surname_2 }}, {{ fourth_initials }} {{ fourth_surname }}
            {% else %}
                {% if second_surname_4 or second_initials_4 %}
                    {{ title }}{% if parallel %} = {{ parallel }}{% endif %}{% if type_doc %} : {{ type_doc }}{% endif %}{% if explanations %} : [{{ explanations }}]{% endif %} / {{ initials }} {{ surname }}, {{ second_initials_4 }} {{ second_surname_4 }}, {{ third_initials_3 }} {{ third_surname_3 }} [и др.]
                {% else %}
                    {% if second_surname_2 or second_initials_2 %}
                        {{ surname }}, {{ initials }} {{ title }}{% if parallel %} = {{ parallel }}{% endif %}{% if type_doc %} : {{ type_doc }}{% endif %}{% if explanations %} : [{{ explanations }}]{% endif %} / {{ initials }} {{ surname }}, {{ second_initials_2 }} {{ second_surname_2 }}, {{ third_initials }} {{ third_surname }}
                    {% else %}
                        {% if second_surname or second_initials %}
                            {{ surname }}, {{ initials }} {{ title }}{% if parallel %} = {{ parallel }}{% endif %}{% if type_doc %} : {{ type_doc }}{% endif %}{% if explanations %} : [{{ explanations }}]{% endif %} / {{ initials }} {{ surname }}, {{ second_initials }} {{ second_surname }}
                        {% else %}
                            {{ surname }}, {{ initials }} {{ title }}{% if parallel %} = {{ parallel }}{% endif %}{% if type_doc %} : {{ type_doc }}{% endif %}{% if explanations %} : [{{ explanations }}]{% endif %} / {{ initials }} {{ surname }}
                        {% endif %}
                    {% endif %}
                {% endif %}
            {% endif %}
        ''',
    },
    'editedbook': { 
        'data': "{{ title }}{% if parallel %} = {{ parallel }}{% endif %}{% if type_doc %} : {{ type_doc }}{% endif %}{% if explanations %} : [{{ explanations }}]{% endif %} / {% if organization %} {{ organization }} ;{% endif %} {{ editor }}{% if responsibility %} ; {{ responsibility }}{% endif %}{% if edit_info %}. – {{ edit_info }}{% endif %}{% if par_edit_info %} = {{ par_edit_info }}{% endif %}{% if liability %} / {{ liability }}{% endif %}. – {{ place }} : {{ publishing }}, {{ year }}{% if place_of_distribution %} ; {{ place_of_distribution }}{% endif %}{% if organization_of_distribution %} : {{ organization_of_distribution }} [распространитель],{% endif %}{% if distribution_date %} {{ distribution_date }}{% endif %}{% if manufacture %} ({{ manufacture }}){% endif %}. – {{ pages }}{% if unnumbered_pages %}, [{{ unnumbered_pages }}]{% endif %} с.{% if illustrations %}, {{ illustrations }}{% endif %}{% if physical_characteristics %} : {{ physical_characteristics }}{% endif %}{% if size %} ; {{ size }} см{% endif %}{% if accompanying %} + {{ accompanying }}{% endif %}{% if main_title %} ({{ main_title }}{% if parallel_series_title %} = {{ parallel_series_title }}{% endif %}{% if series_title_information %} : {{ series_title_information }}{% endif %}{% if responsibility_info %} / {{ responsibility_info }}{% endif %}{% if number %}, {{ number }}{% endif %}{% if serial_number %} ; {{ serial_number }}{% endif %}{% if sub_main_title %}. {{ sub_main_title }}{% endif %}{% if sub_parallel_series_title %} = {{ sub_parallel_series_title }}{% endif %}{% if sub_series_title_information %} : {{ sub_series_title_information }}{% endif %}{% if sub_responsibility_info %} / {{ sub_responsibility_info }}{% endif %}{% if sub_number %}, {{ sub_number }}{% endif %}{% if sub_serial_number %} ; {{ sub_serial_number }}{% endif %}){% endif %}{% if notes %}. – {{ notes }}{% endif %}{% if general_notes %}. – {{ general_notes }}{% endif %}{% if isbn %} – ISBN {{ isbn }}{% endif %}{% if additional_information %} ({{ additional_information }}){% endif %}{% if fingerprint %}. – Фингерпринт: {{ fingerprint }}{% endif %}{% if availability %} : {{ availability }}{% endif %}{% if content %}. – {{ content }}{% endif %}{% if content_type %} ({{ content_type }}){% endif %}{% if access_means %} : {{ access_means }}{% endif %}"
    },
    'electronicbook': { 
        'data': '{% if responsibility %} ; {{ responsibility }}{% endif %}{% if edit_info %}. – {{ edit_info }}{% endif %}{% if par_edit_info %} = {{ par_edit_info }}{% endif %}{% if liability %} / {{ liability }}{% endif %}. – {{ place }} : {{ publishing }}, {{ year }}{% if place_of_distribution %} ; {{ place_of_distribution }}{% endif %}{% if organization_of_distribution %} : {{ organization_of_distribution }} [распространитель],{% endif %}{% if distribution_date %} {{ distribution_date }}{% endif %}{% if manufacture %} ({{ manufacture }}){% endif %}. – {{ pages }}{% if unnumbered_pages %}, [{{ unnumbered_pages }}]{% endif %} с.{% if illustrations %}, {{ illustrations }}{% endif %} – URL: {{ url }} (дата обращения: {{ date }}){% if access_mode %}. – Режим доступа: {{ access_mode }}{% endif %}{% if main_title %} ({{ main_title }}{% if parallel_series_title %} = {{ parallel_series_title }}{% endif %}{% if series_title_information %} : {{ series_title_information }}{% endif %}{% if responsibility_info %} / {{ responsibility_info }}{% endif %}{% if number %}, {{ number }}{% endif %}{% if serial_number %} ; {{ serial_number }}{% endif %}{% if sub_main_title %}. {{ sub_main_title }}{% endif %}{% if sub_parallel_series_title %} = {{ sub_parallel_series_title }}{% endif %}{% if sub_series_title_information %} : {{ sub_series_title_information }}{% endif %}{% if sub_responsibility_info %} / {{ sub_responsibility_info }}{% endif %}{% if sub_number %}, {{ sub_number }}{% endif %}{% if sub_serial_number %} ; {{ sub_serial_number }}{% endif %}){% endif %}{% if notes %}. – {{ notes }}{% endif %}{% if general_notes %}. – {{ general_notes }}{% endif %}{% if isbn %} – ISBN {{ isbn }}{% endif %}{% if additional_information %} ({{ additional_information }}){% endif %}{% if fingerprint %}. – Фингерпринт: {{ fingerprint }}{% endif %}{% if availability %} : {{ availability }}{% endif %}{% if content %}. – {{ content }}{% endif %}{% if content_type %} ({{ content_type }}){% endif %}{% if access_means %} : {{ access_means }}{% endif %}',
        'authors': '''
            {% if fourth_surname or fourth_initials %}
                {{ title }}{% if parallel %} = {{ parallel }}{% endif %}{% if type_doc %} : {{ type_doc }}{% endif %}{% if explanations %} : [{{ explanations }}]{% endif %} / {{ initials }} {{ surname }}, {{ second_initials_3 }} {{ second_surname_3 }}, {{ third_initials_2 }} {{ third_surname_2 }}, {{ fourth_initials }} {{ fourth_surname }}
            {% else %}
                {% if second_surname_4 or second_initials_4 %}
                    {% if parallel %} = {{ parallel }}{% endif %}{% if type_doc %} : {{ type_doc }}{% endif %}{% if explanations %} : [{{ explanations }}]{% endif %} / {{ initials }} {{ surname }}, {{ second_initials_4 }} {{ second_surname_4 }}, {{ third_initials_3 }} {{ third_surname_3 }} [и др.]
                {% else %}
                    {% if second_surname_2 or second_initials_2 %}
                        {{ surname }}, {{ initials }} {{ title }}{% if parallel %} = {{ parallel }}{% endif %}{% if type_doc %} : {{ type_doc }}{% endif %}{% if explanations %} : [{{ explanations }}]{% endif %} / {{ initials }} {{ surname }}, {{ second_initials_2 }} {{ second_surname_2 }}, {{ third_initials }} {{ third_surname }}
                    {% else %}
                        {% if second_surname or second_initials %}
                            {{ surname }}, {{ initials }} {{ title }}{% if parallel %} = {{ parallel }}{% endif %}{% if type_doc %} : {{ type_doc }}{% endif %}{% if explanations %} : [{{ explanations }}]{% endif %} / {{ initials }} {{ surname }}, {{ second_initials }} {{ second_surname }}
                        {% else %}
                            {{ surname }}, {{ initials }} {{ title }}{% if parallel %} = {{ parallel }}{% endif %}{% if type_doc %} : {{ type_doc }}{% endif %}{% if explanations %} : [{{ explanations }}]{% endif %} / {{ initials }} {{ surname }}
                        {% endif %}
                    {% endif %}
                {% endif %}
            {% endif %}
        '''
    },
    'chapter': { 
        'data': '{% if responsibility %} ; {{ responsibility }}{% endif %}{% if edit_info %}. – {{ edit_info }}{% endif %}{% if par_edit_info %} = {{ par_edit_info }}{% endif %}{% if liability %} / {{ liability }}{% endif %}. – {{ place }} : {{ publishing }}, {{ year }}{% if place_of_distribution %} ; {{ place_of_distribution }}{% endif %}{% if organization_of_distribution %} : {{ organization_of_distribution }} [распространитель],{% endif %}{% if distribution_date %} {{ distribution_date }}{% endif %}{% if manufacture %} ({{ manufacture }}){% endif %}. – {{ section }}. – С. {{ pages }}.{% if notes %} – {{ notes }}{% endif %}{% if general_notes %}. – {{ general_notes }}{% endif %}{% if isbn %} – ISBN {{ isbn }}{% endif %}{% if additional_information %} ({{ additional_information }}){% endif %}{% if fingerprint %}. – Фингерпринт: {{ fingerprint }}{% endif %}{% if availability %} : {{ availability }}{% endif %}{% if content %}. – {{ content }}{% endif %}{% if content_type %} ({{ content_type }}){% endif %}{% if access_means %} : {{ access_means }}{% endif %}',
        'authors': '''
            {% if fourth_surname or fourth_initials %}
                {{ surname_chapter }} {{ initials_chapter }} {{ section_title }} / {{ initials_chapter }} {{ surname_chapter }} // {{ title }}{% if parallel %} = {{ parallel }}{% endif %}{% if type_doc %} : {{ type_doc }}{% endif %}{% if explanations %} : [{{ explanations }}]{% endif %} / {{ initials }} {{ surname }}, {{ second_initials_3 }} {{ second_surname_3 }}, {{ third_initials_2 }} {{ third_surname_2 }}, {{ fourth_initials }} {{ fourth_surname }}
            {% else %}
                {% if second_surname_4 or second_initials_4 %}
                    {{ surname_chapter }} {{ initials_chapter }} {{ section_title }} / {{ initials_chapter }} {{ surname_chapter }} // {{ title }}{% if parallel %} = {{ parallel }}{% endif %}{% if type_doc %} : {{ type_doc }}{% endif %}{% if explanations %} : [{{ explanations }}]{% endif %} / {{ initials }} {{ surname }}, {{ second_initials_4 }} {{ second_surname_4 }}, {{ third_initials_3 }} {{ third_surname_3 }} [и др.]
                {% else %}
                    {% if second_surname_2 or second_initials_2 %}
                        {{ surname_chapter }} {{ initials_chapter }} {{ section_title }} / {{ initials_chapter }} {{ surname_chapter }} // {{ title }}{% if parallel %} = {{ parallel }}{% endif %}{% if type_doc %} : {{ type_doc }}{% endif %}{% if explanations %} : [{{ explanations }}]{% endif %} / {{ initials }} {{ surname }}, {{ second_initials_2 }} {{ second_surname_2 }}, {{ third_initials }} {{ third_surname }}
                    {% else %}
                        {% if second_surname or second_initials %}
                            {{ surname_chapter }} {{ initials_chapter }} {{ section_title }} / {{ initials_chapter }} {{ surname_chapter }} // {{ title }}{% if parallel %} = {{ parallel }}{% endif %}{% if type_doc %} : {{ type_doc }}{% endif %}{% if explanations %} : [{{ explanations }}]{% endif %} / {{ initials }} {{ surname }}, {{ second_initials }} {{ second_surname }}
                        {% else %}
                            {{ surname_chapter }} {{ initials_chapter }} {{ section_title }} / {{ initials_chapter }} {{ surname_chapter }} // {{ title }}{% if parallel %} = {{ parallel }}{% endif %}{% if type_doc %} : {{ type_doc }}{% endif %}{% if explanations %} : [{{ explanations }}]{% endif %} / {{ initials }} {{ surname }}
                        {% endif %}
                    {% endif %}
                {% endif %}
            {% endif %}
        '''
    },
    'multivolume': { 
        'data': '{% if responsibility %} ; {{ responsibility }}{% endif %}{% if edit_info %}. – {{ edit_info }}{% endif %}{% if par_edit_info %} = {{ par_edit_info }}{% endif %}{% if liability %} / {{ liability }}{% endif %}. – {{ place }} : {{ publishing }}, {{ year }}{% if place_of_distribution %} ; {{ place_of_distribution }}{% endif %}{% if organization_of_distribution %} : {{ organization_of_distribution }} [распространитель],{% endif %}{% if distribution_date %} {{ distribution_date }}{% endif %}{% if manufacture %} ({{ manufacture }}){% endif %}. – {{ pages }}{% if unnumbered_pages %}, [{{ unnumbered_pages }}]{% endif %} с.{% if illustrations %}, {{ illustrations }}{% endif %}{% if physical_characteristics %} : {{ physical_characteristics }}{% endif %}{% if size %} ; {{ size }} см{% endif %}{% if accompanying %} + {{ accompanying }}{% endif %}{% if main_title %} ({{ main_title }}{% if parallel_series_title %} = {{ parallel_series_title }}{% endif %}{% if series_title_information %} : {{ series_title_information }}{% endif %}{% if responsibility_info %} / {{ responsibility_info }}{% endif %}{% if number %}, {{ number }}{% endif %}{% if serial_number %} ; {{ serial_number }}{% endif %}{% if sub_main_title %}. {{ sub_main_title }}{% endif %}{% if sub_parallel_series_title %} = {{ sub_parallel_series_title }}{% endif %}{% if sub_series_title_information %} : {{ sub_series_title_information }}{% endif %}{% if sub_responsibility_info %} / {{ sub_responsibility_info }}{% endif %}{% if sub_number %}, {{ sub_number }}{% endif %}{% if sub_serial_number %} ; {{ sub_serial_number }}{% endif %}){% endif %}{% if notes %}. – {{ notes }}{% endif %}{% if general_notes %}. – {{ general_notes }}{% endif %}{% if isbn %} – ISBN {{ isbn }}{% endif %}{% if additional_information %} ({{ additional_information }}){% endif %}{% if fingerprint %}. – Фингерпринт: {{ fingerprint }}{% endif %}{% if availability %} : {{ availability }}{% endif %}{% if content %}. – {{ content }}{% endif %}{% if content_type %} ({{ content_type }}){% endif %}{% if access_means %} : {{ access_means }}{% endif %} ',
        'authors': '''
            {% if fourth_surname or fourth_initials %}
                {{ title }}{% if parallel %} = {{ parallel }}{% endif %}{% if type_doc %} : {{ type_doc }}{% endif %}{% if explanations %} : [{{ explanations }}]{% endif %} : [в {{ chapters }} томах] / {{ initials }} {{ surname }}, {{ second_initials_3 }} {{ second_surname_3 }}, {{ third_initials_2 }} {{ third_surname_2 }}, {{ fourth_initials }} {{ fourth_surname }}
            {% else %}
                {% if second_surname_4 or second_initials_4 %}
                    {{ title }}{% if parallel %} = {{ parallel }}{% endif %}{% if type_doc %} : {{ type_doc }}{% endif %}{% if explanations %} : [{{ explanations }}]{% endif %} : [в {{ chapters }} томах] / {{ initials }} {{ surname }}, {{ second_initials_4 }} {{ second_surname_4 }}, {{ third_initials_3 }} {{ third_surname_3 }} [и др.]
                {% else %}
                    {% if second_surname_2 or second_initials_2 %}
                        {{ surname }}, {{ initials }} {{ title }}{% if parallel %} = {{ parallel }}{% endif %}{% if type_doc %} : {{ type_doc }}{% endif %}{% if explanations %} : [{{ explanations }}]{% endif %} : [в {{ chapters }} томах] / {{ initials }} {{ surname }}, {{ second_initials_2 }} {{ second_surname_2 }}, {{ third_initials }} {{ third_surname }}
                    {% else %}
                        {% if second_surname or second_initials %}
                            {{ surname }}, {{ initials }} {{ title }}{% if parallel %} = {{ parallel }}{% endif %}{% if type_doc %} : {{ type_doc }}{% endif %}{% if explanations %} : [{{ explanations }}]{% endif %} : [в {{ chapters }} томах] / {{ initials }} {{ surname }}, {{ second_initials }} {{ second_surname }}
                        {% else %}
                            {{ surname }}, {{ initials }} {{ title }}{% if parallel %} = {{ parallel }}{% endif %}{% if type_doc %} : {{ type_doc }}{% endif %}{% if explanations %} : [{{ explanations }}]{% endif %} : [в {{ chapters }} томах] / {{ initials }} {{ surname }}
                        {% endif %}
                    {% endif %}
                {% endif %}
            {% endif %}
        '''
    },
    'volume': { 
        'data': '{% if responsibility %} ; {{ responsibility }}{% endif %}{% if edit_info %}. – {{ edit_info }}{% endif %}{% if par_edit_info %} = {{ par_edit_info }}{% endif %}{% if liability %} / {{ liability }}{% endif %}. – {{ place }} : {{ publishing }}, {{ year }}{% if place_of_distribution %} ; {{ place_of_distribution }}{% endif %}{% if organization_of_distribution %} : {{ organization_of_distribution }} [распространитель],{% endif %}{% if distribution_date %} {{ distribution_date }}{% endif %}{% if manufacture %} ({{ manufacture }}){% endif %}. – {{ pages }}{% if unnumbered_pages %}, [{{ unnumbered_pages }}]{% endif %} с.{% if illustrations %}, {{ illustrations }}{% endif %}{% if physical_characteristics %} : {{ physical_characteristics }}{% endif %}{% if size %} ; {{ size }} см{% endif %}{% if accompanying %} + {{ accompanying }}{% endif %}{% if main_title %} ({{ main_title }}{% if parallel_series_title %} = {{ parallel_series_title }}{% endif %}{% if series_title_information %} : {{ series_title_information }}{% endif %}{% if responsibility_info %} / {{ responsibility_info }}{% endif %}{% if number %}, {{ number }}{% endif %}{% if serial_number %} ; {{ serial_number }}{% endif %}{% if sub_main_title %}. {{ sub_main_title }}{% endif %}{% if sub_parallel_series_title %} = {{ sub_parallel_series_title }}{% endif %}{% if sub_series_title_information %} : {{ sub_series_title_information }}{% endif %}{% if sub_responsibility_info %} / {{ sub_responsibility_info }}{% endif %}{% if sub_number %}, {{ sub_number }}{% endif %}{% if sub_serial_number %} ; {{ sub_serial_number }}{% endif %}){% endif %}{% if notes %}. – {{ notes }}{% endif %}{% if general_notes %}. – {{ general_notes }}{% endif %}{% if isbn %} – ISBN {{ isbn }}{% endif %}{% if additional_information %} ({{ additional_information }}){% endif %}{% if fingerprint %}. – Фингерпринт: {{ fingerprint }}{% endif %}{% if availability %} : {{ availability }}{% endif %}{% if content %}. – {{ content }}{% endif %}{% if content_type %} ({{ content_type }}){% endif %}{% if access_means %} : {{ access_means }}{% endif %}',
        'authors': '''
            {% if fourth_surname or fourth_initials %} 
                {{ title }}{% if parallel %} = {{ parallel }}{% endif %}{% if type_doc %} : {{ type_doc }}{% endif %}{% if explanations %} : [{{ explanations }}]{% endif %}. В {{ chapters }} т. Т. {{ n_volume }} / {{ initials }} {{ surname }}, {{ second_initials_3 }} {{ second_surname_3 }}, {{ third_initials_2 }} {{ third_surname_2 }}, {{ fourth_initials }} {{ fourth_surname }}
            {% else %} 
                {% if second_surname_4 or second_initials_4 %} 
                    {{ title }}{% if parallel %} = {{ parallel }}{% endif %}{% if type_doc %} : {{ type_doc }}{% endif %}{% if explanations %} : [{{ explanations }}]{% endif %}. В {{ chapters }} т. Т. {{ n_volume }} / {{ initials }} {{ surname }}, {{ second_initials_4 }} {{ second_surname_4 }}, {{ third_initials_3 }} {{ third_surname_3 }} [и др.]
                {% else %}
                    {% if second_surname_2 or second_initials_2 %}
                        {{ surname }}, {{ initials }} {{ title }}{% if parallel %} = {{ parallel }}{% endif %}{% if type_doc %} : {{ type_doc }}{% endif %}{% if explanations %} : [{{ explanations }}]{% endif %}. В {{ chapters }} т. Т. {{ n_volume }} / {{ initials }} {{ surname }}, {{ second_initials_2 }} {{ second_surname_2 }}, {{ third_initials }} {{ third_surname }}
                    {% else %} 
                        {% if second_surname or second_initials %} 
                            {{ surname }}, {{ initials }} {{ title }}{% if parallel %} = {{ parallel }}{% endif %}{% if type_doc %} : {{ type_doc }}{% endif %}{% if explanations %} : [{{ explanations }}]{% endif %}. В {{ chapters }} т. Т. {{ n_volume }} / {{ initials }} {{ surname }}, {{ second_initials }} {{ second_surname }}
                        {% else %} 
                            {{ surname }}, {{ initials }} {{ title }}{% if parallel %} = {{ parallel }}{% endif %}{% if type_doc %} : {{ type_doc }}{% endif %}{% if explanations %} : [{{ explanations }}]{% endif %}. В {{ chapters }} т. Т. {{ n_volume }} / {{ initials }} {{ surname }}
                        {% endif %}
                    {% endif %}
                {% endif %}
            {% endif %}
        '''
    },
    'magazinearticle': { # !!!
        'data': '{% if responsibility_info %} / {{ responsibility_info }}{% endif %}{% if number %}, {{ number }}{% endif %}{% if serial_number %} ; {{ serial_number }}{% endif %}{% if sub_main_title %}. {{ sub_main_title }}{% endif %}{% if sub_parallel_series_title %} = {{ sub_parallel_series_title }}{% endif %}{% if sub_series_title_information %} : {{ sub_series_title_information }}{% endif %}{% if sub_responsibility_info %} / {{ sub_responsibility_info }}{% endif %}{% if sub_number %}, {{ sub_number }}{% endif %}{% if sub_serial_number %} ; {{ sub_serial_number }}{% endif %}){% endif %}{% if issn %} – ISSN {{ issn }}{% endif %}{% if doi %} – DOI {{ doi }}{% endif %}{% if key_title %} = {{ key_title }}{% endif %}{% if additional_information %} ({{ additional_information }}){% endif %}{% if availability %} : {{ availability }}{% endif %}{% if content %}. – {{ content }}{% endif %}{% if content_type %} ({{ content_type }}){% endif %}{% if access_means %} : {{ access_means }}{% endif %}',
        'authors': '''
            {% if fourth_surname or fourth_initials %}
                {{ title }}{% if parallel %} = {{ parallel }}{% endif %}{% if explanations %} : [{{ explanations }}]{% endif %} / {{ initials }} {{ surname }}, {{ second_initials_3 }} {{ second_surname_3 }}, {{ third_initials_2 }} {{ third_surname_2 }}, {{ fourth_initials }} {{ fourth_surname }} // {{ journal_title }}. – {{ year }}. –{% if volume_n %} Т. {{ volume_n }},{% endif %} № {{ issue }}. – С. {{ pages }}.{% if size %} ; {{ size }} см{% endif %}{% if main_title %} ({{ main_title }}{% if parallel_series_title %} = {{ parallel_series_title }}{% endif %}{% if series_title_information %} : {{ series_title_information }}{% endif %}
            {% else %}
                {% if second_surname_4 or second_initials_4 %}
                    {{ title }}{% if parallel %} = {{ parallel }}{% endif %}{% if explanations %} : [{{ explanations }}]{% endif %} / {{ initials }} {{ surname }}, {{ second_initials_4 }} {{ second_surname_4 }}, {{ third_initials_3 }} {{ third_surname_3 }} [и др.] // {{ journal_title }}. – {{ year }}. –{% if volume_n %} Т. {{ volume_n }},{% endif %} № {{ issue }}. – С. {{ pages }}.{% if size %} ; {{ size }} см{% endif %}{% if main_title %} ({{ main_title }}{% if parallel_series_title %} = {{ parallel_series_title }}{% endif %}{% if series_title_information %} : {{ series_title_information }}{% endif %}
                {% else %}
                    {% if second_surname_2 or second_initials_2 %}
                        {{ surname }}, {{ initials }} {{ title }}{% if parallel %} = {{ parallel }}{% endif %}{% if explanations %} : [{{ explanations }}]{% endif %} / {{ initials }} {{ surname }}, {{ second_initials_2 }} {{ second_surname_2 }}, {{ third_initials }} {{ third_surname }} // {{ journal_title }}. – {{ year }}. –{% if volume_n %} Т. {{ volume_n }},{% endif %} № {{ issue }}. – С. {{ pages }}.{% if size %} ; {{ size }} см{% endif %}{% if main_title %} ({{ main_title }}{% if parallel_series_title %} = {{ parallel_series_title }}{% endif %}{% if series_title_information %} : {{ series_title_information }}{% endif %}
                    {% else %}
                        {% if second_surname or second_initials %}
                            {{ surname }}, {{ initials }} {{ title }}{% if parallel %} = {{ parallel }}{% endif %}{% if explanations %} : [{{ explanations }}]{% endif %} / {{ initials }} {{ surname }}, {{ second_initials }} {{ second_surname }} // {{ journal_title }}. – {{ year }}. –{% if volume_n %} Т. {{ volume_n }},{% endif %} № {{ issue }}. – С. {{ pages }}.{% if size %} ; {{ size }} см{% endif %}{% if main_title %} ({{ main_title }}{% if parallel_series_title %} = {{ parallel_series_title }}{% endif %}{% if series_title_information %} : {{ series_title_information }}{% endif %}
                        {% else %}
                            {{ surname }}, {{ initials }} {{ title }}{% if parallel %} = {{ parallel }}{% endif %}{% if explanations %} : [{{ explanations }}]{% endif %} / {{ initials }} {{ surname }} // {{ journal_title }}. – {{ year }}. –{% if volume_n %} Т. {{ volume_n }},{% endif %} № {{ issue }}. – С. {{ pages }}.{% if size %} ; {{ size }} см{% endif %}{% if main_title %} ({{ main_title }}{% if parallel_series_title %} = {{ parallel_series_title }}{% endif %}{% if series_title_information %} : {{ series_title_information }}{% endif %}
                        {% endif %}
                    {% endif %}
                {% endif %}
            {% endif %} 
        ''' 
    },
    'newspaperarticle': { 
        'data': '{% if responsibility_info %} / {{ responsibility_info }}{% endif %}{% if number %}, {{ number }}{% endif %}{% if serial_number %} ; {{ serial_number }}{% endif %}{% if sub_main_title %}. {{ sub_main_title }}{% endif %}{% if sub_parallel_series_title %} = {{ sub_parallel_series_title }}{% endif %}{% if sub_series_title_information %} : {{ sub_series_title_information }}{% endif %}{% if sub_responsibility_info %} / {{ sub_responsibility_info }}{% endif %}{% if sub_number %}, {{ sub_number }}{% endif %}{% if sub_serial_number %} ; {{ sub_serial_number }}{% endif %}){% endif %}{% if issn %} – ISSN {{ issn }}{% endif %}{% if doi %} – DOI {{ doi }}{% endif %}{% if key_title %} = {{ key_title }}{% endif %}{% if additional_information %} ({{ additional_information }}){% endif %}{% if availability %} : {{ availability }}{% endif %}',
        'authors': '''
            {% if fourth_surname or fourth_initials %}
                {{ title }}{% if parallel %} = {{ parallel }}{% endif %}{% if explanations %} : [{{ explanations }}]{% endif %} / {{ initials }} {{ surname }}, {{ second_initials_3 }} {{ second_surname_3 }}, {{ third_initials_2 }} {{ third_surname_2 }}, {{ fourth_initials }} {{ fourth_surname }}{% if content %}. – {{ content }}{% endif %}{% if content_type %} ({{ content_type }}){% endif %}{% if access_means %} : {{ access_means }}{% endif %} // {{ journal_title }}{% if year %}. – {{ year }}{% endif %}{% if issue %}. – № {{ issue }}{% endif %}{% if pages %}. – С. {{ pages }}.{% endif %}{% if date %}. – {{ date }}{% endif %}{% if size %} ; {{ size }} см{% endif %}{% if main_title %} ({{ main_title }}{% if parallel_series_title %} = {{ parallel_series_title }}{% endif %}{% if series_title_information %} : {{ series_title_information }}{% endif %}
            {% else %}
                {% if second_surname_4 or second_initials_4 %}
                    {{ title }}{% if parallel %} = {{ parallel }}{% endif %}{% if explanations %} : [{{ explanations }}]{% endif %} / {{ initials }} {{ surname }}, {{ second_initials_4 }} {{ second_surname_4 }}, {{ third_initials_3 }} {{ third_surname_3 }} [и др.]{% if content %}. – {{ content }}{% endif %}{% if content_type %} ({{ content_type }}){% endif %}{% if access_means %} : {{ access_means }}{% endif %} // {{ journal_title }}{% if year %}. – {{ year }}{% endif %}{% if issue %}. – № {{ issue }}{% endif %}{% if pages %}. – С. {{ pages }}.{% endif %}{% if date %}. – {{ date }}{% endif %}{% if size %} ; {{ size }} см{% endif %}{% if main_title %} ({{ main_title }}{% if parallel_series_title %} = {{ parallel_series_title }}{% endif %}{% if series_title_information %} : {{ series_title_information }}{% endif %}
                {% else %}
                    {% if second_surname_2 or second_initials_2 %}
                        {{ surname }}, {{ initials }} {{ title }}{% if parallel %} = {{ parallel }}{% endif %}{% if explanations %} : [{{ explanations }}]{% endif %} / {{ initials }} {{ surname }}, {{ second_initials_2 }} {{ second_surname_2 }}, {{ third_initials }} {{ third_surname }}{% if content %}. – {{ content }}{% endif %}{% if content_type %} ({{ content_type }}){% endif %}{% if access_means %} : {{ access_means }}{% endif %} // {{ journal_title }}{% if year %}. – {{ year }}{% endif %}{% if issue %}. – № {{ issue }}{% endif %}{% if pages %}. – С. {{ pages }}.{% endif %}{% if date %}. – {{ date }}{% endif %}{% if size %} ; {{ size }} см{% endif %}{% if main_title %} ({{ main_title }}{% if parallel_series_title %} = {{ parallel_series_title }}{% endif %}{% if series_title_information %} : {{ series_title_information }}{% endif %}
                    {% else %}
                        {% if second_surname or second_initials %}
                            {{ surname }}, {{ initials }} {{ title }}{% if parallel %} = {{ parallel }}{% endif %}{% if explanations %} : [{{ explanations }}]{% endif %} / {{ initials }} {{ surname }}, {{ second_initials }} {{ second_surname }}{% if content %}. – {{ content }}{% endif %}{% if content_type %} ({{ content_type }}){% endif %}{% if access_means %} : {{ access_means }}{% endif %} // {{ journal_title }}{% if year %}. – {{ year }}{% endif %}{% if issue %}. – № {{ issue }}{% endif %}{% if pages %}. – С. {{ pages }}.{% endif %}{% if date %}. – {{ date }}{% endif %}{% if size %} ; {{ size }} см{% endif %}{% if main_title %} ({{ main_title }}{% if parallel_series_title %} = {{ parallel_series_title }}{% endif %}{% if series_title_information %} : {{ series_title_information }}{% endif %}
                        {% else %}
                            {{ surname }}, {{ initials }} {{ title }}{% if parallel %} = {{ parallel }}{% endif %}{% if explanations %} : [{{ explanations }}]{% endif %} / {{ initials }} {{ surname }}{% if content %}. – {{ content }}{% endif %}{% if content_type %} ({{ content_type }}){% endif %}{% if access_means %} : {{ access_means }}{% endif %} // {{ journal_title }}{% if year %}. – {{ year }}{% endif %}{% if issue %}. – № {{ issue }}{% endif %}{% if pages %}. – С. {{ pages }}.{% endif %}{% if date %}. – {{ date }}{% endif %}{% if size %} ; {{ size }} см{% endif %}{% if main_title %} ({{ main_title }}{% if parallel_series_title %} = {{ parallel_series_title }}{% endif %}{% if series_title_information %} : {{ series_title_information }}{% endif %}
                        {% endif %}
                    {% endif %}
                {% endif %}
            {% endif %}
        '''
    },
     'collectionarticle': {
        'data': '{% if responsibility %} ; {{ responsibility }}{% endif %}{% if edit_info %}. – {{ edit_info }}{% endif %}{% if par_edit_info %} = {{ par_edit_info }}{% endif %}{% if liability %} / {{ liability }}{% endif %}. – {{ place }}{% if publishing %} : {{ publishing }}{% endif %}, {{ year }}{% if place_of_distribution %} ; {{ place_of_distribution }}{% endif %}{% if organization_of_distribution %} : {{ organization_of_distribution }} [распространитель],{% endif %}{% if distribution_date %} {{ distribution_date }}{% endif %}{% if manufacture %} ({{ manufacture }}){% endif %}. – С. {{ pages }}.{% if illustrations %}, {{ illustrations }}{% endif %}{% if physical_characteristics %} : {{ physical_characteristics }}{% endif %}{% if size %} ; {{ size }} см{% endif %}{% if accompanying %} + {{ accompanying }}{% endif %}{% if main_title %} ({{ main_title }}{% if parallel_series_title %} = {{ parallel_series_title }}{% endif %}{% if series_title_information %} : {{ series_title_information }}{% endif %}{% if responsibility_info %} / {{ responsibility_info }}{% endif %}{% if number %}, {{ number }}{% endif %}{% if serial_number %} ; {{ serial_number }}{% endif %}{% if sub_main_title %}. {{ sub_main_title }}{% endif %}{% if sub_parallel_series_title %} = {{ sub_parallel_series_title }}{% endif %}{% if sub_series_title_information %} : {{ sub_series_title_information }}{% endif %}{% if sub_responsibility_info %} / {{ sub_responsibility_info }}{% endif %}{% if sub_number %}, {{ sub_number }}{% endif %}{% if sub_serial_number %} ; {{ sub_serial_number }}{% endif %}){% endif %}{% if notes %}. – {{ notes }}{% endif %}{% if general_notes %}. – {{ general_notes }}{% endif %}{% if isbn %} – ISBN {{ isbn }}{% endif %}{% if additional_information %} ({{ additional_information }}){% endif %}{% if fingerprint %}. – Фингерпринт: {{ fingerprint }}{% endif %}{% if availability %} : {{ availability }}{% endif %}{% if content %}. – {{ content }}{% endif %}{% if content_type %} ({{ content_type }}){% endif %}{% if access_means %} : {{ access_means }}{% endif %}',
        'authors': '''
            {% if fourth_surname or fourth_initials %}
                {{ title }}{% if parallel %} = {{ parallel }}{% endif %}{% if type_doc %} : {{ type_doc }}{% endif %}{% if explanations %} : [{{ explanations }}]{% endif %} / {{ initials }} {{ surname }}, {{ second_initials_3 }} {{ second_surname_3 }}, {{ third_initials_2 }} {{ third_surname_2 }}, {{ fourth_initials }} {{ fourth_surname }} // {{ collection_title }} 
            {% else %}
                {% if second_surname_4 or second_initials_4 %}
                    {{ title }}{% if parallel %} = {{ parallel }}{% endif %}{% if type_doc %} : {{ type_doc }}{% endif %}{% if explanations %} : [{{ explanations }}]{% endif %} / {{ initials }} {{ surname }}, {{ second_initials_4 }} {{ second_surname_4 }}, {{ third_initials_3 }} {{ third_surname_3 }} [и др.] // {{ collection_title }} 
                {% else %}
                    {% if second_surname_2 or second_initials_2 %}
                        {{ surname }}, {{ initials }} {{ title }}{% if parallel %} = {{ parallel }}{% endif %}{% if type_doc %} : {{ type_doc }}{% endif %}{% if explanations %} : [{{ explanations }}]{% endif %} / {{ initials }} {{ surname }}, {{ second_initials_2 }} {{ second_surname_2 }}, {{ third_initials }} {{ third_surname }} // {{ collection_title }} 
                    {% else %}
                        {% if second_surname or second_initials %}
                            {{ surname }}, {{ initials }} {{ title }}{% if parallel %} = {{ parallel }}{% endif %}{% if type_doc %} : {{ type_doc }}{% endif %}{% if explanations %} : [{{ explanations }}]{% endif %} / {{ initials }} {{ surname }}, {{ second_initials }} {{ second_surname }} // {{ collection_title }} 
                        {% else %}
                            {{ surname }}, {{ initials }} {{ title }}{% if parallel %} = {{ parallel }}{% endif %}{% if type_doc %} : {{ type_doc }}{% endif %}{% if explanations %} : [{{ explanations }}]{% endif %} / {{ initials }} {{ surname }} // {{ collection_title }} 
                        {% endif %}
                    {% endif %}
                {% endif %}
            {% endif %}
        '''
    },
    'site': { 
        'data': '{{ title }}{% if title_info %} : {{ title_info }}{% endif %} :{% if site_type %} {{ site_type }}{% endif %} сайт{% if explanations %} : [{{ explanations }}]{% endif %}.{% if place or year %} – {% if place %}{{ place }}{% endif %}{% if place and year %},{% endif %}{% if year %} {{ year }}{% endif %}.{% endif %} – URL: {{ url }} (дата обращения: {{ date }}){% if availability %}. – Режим доступа: {{ availability }}{% endif %}{% if content %}. – {{ content }}{% endif %}{% if access_means %} : {{ access_means }}{% endif %}',
    },
    'localaccess': { 
        'data': '{{ title }}{% if parallel %} = {{ parallel }}{% endif %}{% if type_doc %} : {{ type_doc }}{% endif %}{% if explanations %} : [{{ explanations }}]{% endif %}{% if responsibility %} ; {{ responsibility }}{% endif %}{% if edit_info %}. – {{ edit_info }}{% endif %}. – {{ place }}, {{ year }}{% if place_of_distribution %} ; {{ place_of_distribution }}{% endif %}{% if organization_of_distribution %} : {{ organization_of_distribution }} [распространитель],{% endif %}{% if distribution_date %} {{ distribution_date }}{% endif %}{% if manufacture %} ({{ manufacture }}){% endif %}.{% if physical_characteristics %} – {{ physical_characteristics }}{% endif %}{% if size %} ; {{ size }} см{% endif %}{% if accompanying %} + {{ accompanying }}{% endif %}{% if source %} – {{ source }}{% endif %}{% if content %}. – {{ content }}{% endif %}{% if content_type %} ({{ content_type }}){% endif %}{% if access_means %} : {{ access_means }}{% endif %}',
    },
    'internetportal': { 
        'data': '{{ title }}{% if title_info %} : {{ title_info }}{% endif %} :{% if site_type %} {{ site_type }}{% endif %} портал{% if explanations %} : [{{ explanations }}]{% endif %}{% if responsibility %} / {{ responsibility }}{% endif %}{% if content %}. – {{ content }}{% endif %}{% if access_means %} : {{ access_means }}{% endif %}.{% if place or year %} – {% if place %}{{ place }}{% endif %}{% if place and year %},{% endif %}{% if year %} {{ year }}{% endif %}.{% endif %} – URL: {{ url }} (дата обращения: {{ date }}){% if availability %}. – Режим доступа: {{ availability }}{% endif %}',
    },
    'electronicjournal': { 
        'data': '{% if responsibility_info %} / {{ responsibility_info }}{% endif %}{% if number %}, {{ number }}{% endif %}{% if serial_number %} ; {{ serial_number }}{% endif %}{% if sub_main_title %}. {{ sub_main_title }}{% endif %}{% if sub_parallel_series_title %} = {{ sub_parallel_series_title }}{% endif %}{% if sub_series_title_information %} : {{ sub_series_title_information }}{% endif %}{% if sub_responsibility_info %} / {{ sub_responsibility_info }}{% endif %}{% if sub_number %}, {{ sub_number }}{% endif %}{% if sub_serial_number %} ; {{ sub_serial_number }}{% endif %}){% endif %}{% if issn %} – ISSN {{ issn }}{% endif %}{% if doi %} – DOI {{ doi }}{% endif %}{% if key_title %} = {{ key_title }}{% endif %}{% if additional_information %} ({{ additional_information }}){% endif %}{% if availability %} : {{ availability }}{% endif %}',
        'authors': '''
            {% if fourth_surname or fourth_initials %}
                {{ title }}{% if parallel %} = {{ parallel }}{% endif %}{% if explanations %} : [{{ explanations }}]{% endif %} / {{ initials }} {{ surname }}, {{ second_initials_3 }} {{ second_surname_3 }}, {{ third_initials_2 }} {{ third_surname_2 }}, {{ fourth_initials }} {{ fourth_surname }}{% if content %}. – {{ content }}{% endif %}{% if content_type %} ({{ content_type }}){% endif %}{% if access_means %} : {{ access_means }}{% endif %} // {{ journal_title }} : электронный журнал. – URL: {{ url }}{% if publication_date %}. – Дата публикации: {{ publication_date }}.{% else %} (дата обращения: {date_today}).{% endif %}{% if date %} (дата обращения: {{ date }}){% endif %}{% if main_title %} ({{ main_title }}{% if parallel_series_title %} = {{ parallel_series_title }}{% endif %}{% if series_title_information %} : {{ series_title_information }}{% endif %}
            {% else %}
                {% if second_surname_4 or second_initials_4 %}
                    {{ title }}{% if parallel %} = {{ parallel }}{% endif %}{% if explanations %} : [{{ explanations }}]{% endif %} / {{ initials }} {{ surname }}, {{ second_initials_4 }} {{ second_surname_4 }}, {{ third_initials_3 }} {{ third_surname_3 }} [и др.]{% if content %}. – {{ content }}{% endif %}{% if content_type %} ({{ content_type }}){% endif %}{% if access_means %} : {{ access_means }}{% endif %} // {{ journal_title }} : электронный журнал. – URL: {{ url }}{% if publication_date %}. – Дата публикации: {{ publication_date }}.{% else %} (дата обращения: {date_today}).{% endif %}{% if date %} (дата обращения: {{ date }}){% endif %}{% if main_title %} ({{ main_title }}{% if parallel_series_title %} = {{ parallel_series_title }}{% endif %}{% if series_title_information %} : {{ series_title_information }}{% endif %}
                {% else %}
                    {% if second_surname_2 or second_initials_2 %}
                        {{ surname }}, {{ initials }} {{ title }}{% if parallel %} = {{ parallel }}{% endif %}{% if explanations %} : [{{ explanations }}]{% endif %} / {{ initials }} {{ surname }}, {{ second_initials_2 }} {{ second_surname_2 }}, {{ third_initials }} {{ third_surname }}{% if content %}. – {{ content }}{% endif %}{% if content_type %} ({{ content_type }}){% endif %}{% if access_means %} : {{ access_means }}{% endif %} // {{ journal_title }} : электронный журнал. – URL: {{ url }}{% if publication_date %}. – Дата публикации: {{ publication_date }}.{% else %} (дата обращения: {date_today}).{% endif %}{% if date %} (дата обращения: {{ date }}){% endif %}{% if main_title %} ({{ main_title }}{% if parallel_series_title %} = {{ parallel_series_title }}{% endif %}{% if series_title_information %} : {{ series_title_information }}{% endif %}
                    {% else %}
                        {% if second_surname or second_initials %}
                            {{ surname }}, {{ initials }} {{ title }}{% if parallel %} = {{ parallel }}{% endif %}{% if explanations %} : [{{ explanations }}]{% endif %} / {{ initials }} {{ surname }}, {{ second_initials }} {{ second_surname }}{% if content %}. – {{ content }}{% endif %}{% if content_type %} ({{ content_type }}){% endif %}{% if access_means %} : {{ access_means }}{% endif %} // {{ journal_title }} : электронный журнал. – URL: {{ url }}{% if publication_date %}. – Дата публикации: {{ publication_date }}.{% else %} (дата обращения: {date_today}).{% endif %}{% if date %} (дата обращения: {{ date }}){% endif %}{% if main_title %} ({{ main_title }}{% if parallel_series_title %} = {{ parallel_series_title }}{% endif %}{% if series_title_information %} : {{ series_title_information }}{% endif %}
                        {% else %}
                            {{ surname }}, {{ initials }} {{ title }}{% if parallel %} = {{ parallel }}{% endif %}{% if explanations %} : [{{ explanations }}]{% endif %} / {{ initials }} {{ surname }}{% if content %}. – {{ content }}{% endif %}{% if content_type %} ({{ content_type }}){% endif %}{% if access_means %} : {{ access_means }}{% endif %} // {{ journal_title }} : электронный журнал. – URL: {{ url }}{% if publication_date %}. – Дата публикации: {{ publication_date }}. {% else %} (дата обращения: {date_today}).{% endif %}{% if date %} (дата обращения: {{ date }}){% endif %}{% if main_title %} ({{ main_title }}{% if parallel_series_title %} = {{ parallel_series_title }}{% endif %}{% if series_title_information %} : {{ series_title_information }}{% endif %}
                        {% endif %}
                    {% endif %}
                {% endif %}
            {% endif %}
        '''
    },
    'electronicnewspaper': { 
        'data': '{% if responsibility_info %} / {{ responsibility_info }}{% endif %}{% if number %}, {{ number }}{% endif %}{% if serial_number %} ; {{ serial_number }}{% endif %}{% if sub_main_title %}. {{ sub_main_title }}{% endif %}{% if sub_parallel_series_title %} = {{ sub_parallel_series_title }}{% endif %}{% if sub_series_title_information %} : {{ sub_series_title_information }}{% endif %}{% if sub_responsibility_info %} / {{ sub_responsibility_info }}{% endif %}{% if sub_number %}, {{ sub_number }}{% endif %}{% if sub_serial_number %} ; {{ sub_serial_number }}{% endif %}){% endif %}{% if issn %} – ISSN {{ issn }}{% endif %}{% if doi %} – DOI {{ doi }}{% endif %}{% if key_title %} = {{ key_title }}{% endif %}{% if additional_information %} ({{ additional_information }}){% endif %}{% if availability %} : {{ availability }}{% endif %}',
        'authors': '''
            {% if fourth_surname or fourth_initials %}
                {{ title }}{% if parallel %} = {{ parallel }}{% endif %}{% if explanations %} : [{{ explanations }}]{% endif %} / {{ initials }} {{ surname }}, {{ second_initials_3 }} {{ second_surname_3 }}, {{ third_initials_2 }} {{ third_surname_2 }}, {{ fourth_initials }} {{ fourth_surname }}{% if content %}. – {{ content }}{% endif %}{% if content_type %} ({{ content_type }}){% endif %}{% if access_means %} : {{ access_means }}{% endif %} // {{ journal_title }}{% if year %}. – {{ year }}{% endif %}{% if issue %}. – № {{ issue }}{% endif %}{% if pages %}. – С. {{ pages }}.{% endif %}{% if date %}{% endif %}. – {{ date }}. – URL: {{ url }} (дата обращения: {{ application_date }}).{% if main_title %} ({{ main_title }}{% if parallel_series_title %} = {{ parallel_series_title }}{% endif %}{% if series_title_information %} : {{ series_title_information }}{% endif %}
            {% else %}
                {% if second_surname_4 or second_initials_4 %}
                    {{ title }}{% if parallel %} = {{ parallel }}{% endif %}{% if explanations %} : [{{ explanations }}]{% endif %} / {{ initials }} {{ surname }}, {{ second_initials_4 }} {{ second_surname_4 }}, {{ third_initials_3 }} {{ third_surname_3 }} [и др.]{% if content %}. – {{ content }}{% endif %}{% if content_type %} ({{ content_type }}){% endif %}{% if access_means %} : {{ access_means }}{% endif %} // {{ journal_title }}{% if year %}. – {{ year }}{% endif %}{% if issue %}. – № {{ issue }}{% endif %}{% if pages %}. – С. {{ pages }}.{% endif %}{% if date %}. – {{ date }}{% endif %}. – URL: {{ url }} (дата обращения: {{ application_date }}).{% if main_title %} ({{ main_title }}{% if parallel_series_title %} = {{ parallel_series_title }}{% endif %}{% if series_title_information %} : {{ series_title_information }}{% endif %}
                {% else %}
                    {% if second_surname_2 or second_initials_2 %}
                        {{ surname }}, {{ initials }} {{ title }}{% if parallel %} = {{ parallel }}{% endif %}{% if explanations %} : [{{ explanations }}]{% endif %} / {{ initials }} {{ surname }}, {{ second_initials_2 }} {{ second_surname_2 }}, {{ third_initials }} {{ third_surname }}{% if content %}. – {{ content }}{% endif %}{% if content_type %} ({{ content_type }}){% endif %}{% if access_means %} : {{ access_means }}{% endif %} // {{ journal_title }}{% if year %}. – {{ year }}{% endif %}{% if issue %}. – № {{ issue }}{% endif %}{% if pages %}. – С. {{ pages }}.{% endif %}{% if date %}. – {{ date }}{% endif %}. – URL: {{ url }} (дата обращения: {{ application_date }}).{% if main_title %} ({{ main_title }}{% if parallel_series_title %} = {{ parallel_series_title }}{% endif %}{% if series_title_information %} : {{ series_title_information }}{% endif %}
                    {% else %}
                        {% if second_surname or second_initials %}
                            {{ surname }}, {{ initials }} {{ title }}{% if parallel %} = {{ parallel }}{% endif %}{% if explanations %} : [{{ explanations }}]{% endif %} / {{ initials }} {{ surname }}, {{ second_initials }} {{ second_surname }}{% if content %}. – {{ content }}{% endif %}{% if content_type %} ({{ content_type }}){% endif %}{% if access_means %} : {{ access_means }}{% endif %} // {{ journal_title }}{% if year %}. – {{ year }}{% endif %}{% if issue %}. – № {{ issue }}{% endif %}{% if pages %}. – С. {{ pages }}.{% endif %}{% if date %}. – {{ date }}{% endif %}. – URL: {{ url }} (дата обращения: {{ application_date }}).{% if main_title %} ({{ main_title }}{% if parallel_series_title %} = {{ parallel_series_title }}{% endif %}{% if series_title_information %} : {{ series_title_information }}{% endif %}
                        {% else %}
                            {{ surname }}, {{ initials }} {{ title }}{% if parallel %} = {{ parallel }}{% endif %}{% if explanations %} : [{{ explanations }}]{% endif %} / {{ initials }} {{ surname }}{% if content %}. – {{ content }}{% endif %}{% if content_type %} ({{ content_type }}){% endif %}{% if access_means %} : {{ access_means }}{% endif %} // {{ journal_title }}{% if year %}. – {{ year }}{% endif %}{% if issue %}. – № {{ issue }}{% endif %}{% if pages %}. – С. {{ pages }}.{% endif %}{% if date %}. – {{ date }}{% endif %}. – URL: {{ url }} (дата обращения: {{ application_date }}).{% if main_title %} ({{ main_title }}{% if parallel_series_title %} = {{ parallel_series_title }}{% endif %}{% if series_title_information %} : {{ series_title_information }}{% endif %}
                        {% endif %}
                    {% endif %}
                {% endif %}
            {% endif %}
        '''
    },
    'gost': { 
        'data': '{{ title }}{% if introduction %} : {{ introduction }}{% endif %} : дата введения {{ date }}{% if explanations %} : [{{ explanations }}]{% endif %}. – {{ place }} : {{ publishing }}, {{ year }}. – {{ pages }} с.{% if content %} – {{ content }}{% endif %}{% if content_type %} ({{ content_type }}){% endif %}{% if access_means %} : {{ access_means }}{% endif %}',
    },
    'dissertation': { 
        'data': '{{ surname }}, {{ initials }} {{ title }} {% if explanations %} : [{{ explanations }}]{% endif %} : специальность {{ speciality }} : диссертация на соискание {{ competition }} / {{ surname }} {{ full_name }}{% if organization %} ; {{ organization }}{% endif %}. – {{ place }}, {{ year }}. – {{ pages }}{% if unnumbered_pages %}, [{{ unnumbered_pages }}]{% endif %} с.{% if illustrations %}, {{ illustrations }}{% endif %}{% if physical_characteristics %} : {{ physical_characteristics }}{% endif %}{% if bibliography %}. – Библиогр.: с. {{ bibliography }}.{% endif %}{% if content %} – {{ content }}{% endif %}{% if content_type %} ({{ content_type }}){% endif %}{% if access_means %} : {{ access_means }}{% endif %}',
    },
    'dissertationabstract': { 
        'data': '{{ surname }}, {{ initials }} {{ title }} {% if explanations %} : [{{ explanations }}]{% endif %} : специальность {{ speciality }} : автореферат диссертации на соискание {{ competition }} / {{ surname }} {{ full_name }}{% if organization %} ; {{ organization }}{% endif %}. – {{ place }}, {{ year }}. – {{ pages }}{% if unnumbered_pages %}, [{{ unnumbered_pages }}]{% endif %} с.{% if illustrations %}, {{ illustrations }}{% endif %}{% if physical_characteristics %} : {{ physical_characteristics }}{% endif %}{% if bibliography %} – Библиогр.: с. {{ bibliography }}.{% endif %}{% if protection %} – Место защиты: {{ protection }}{% endif %}{% if content %} – {{ content }}{% endif %}{% if content_type %} ({{ content_type }}){% endif %}{% if access_means %} : {{ access_means }}{% endif %}',
    },
    'manual': { 
        'data': '{% if responsibility %} ; {{ responsibility }}{% endif %}{% if edit_info %}. – {{ edit_info }}{% endif %}{% if par_edit_info %} = {{ par_edit_info }}{% endif %}{% if liability %} / {{ liability }}{% endif %}. – {{ place }} : {{ publishing }}, {{ year }}{% if place_of_distribution %} ; {{ place_of_distribution }}{% endif %}{% if organization_of_distribution %} : {{ organization_of_distribution }} [распространитель],{% endif %}{% if distribution_date %} {{ distribution_date }}{% endif %}{% if manufacture %} ({{ manufacture }}){% endif %}. – {{ pages }}{% if unnumbered_pages %}, [{{ unnumbered_pages }}]{% endif %} с.{% if illustrations %}, {{ illustrations }}{% endif %}{% if physical_characteristics %} : {{ physical_characteristics }}{% endif %}{% if size %} ; {{ size }} см{% endif %}{% if accompanying %} + {{ accompanying }}{% endif %}{% if main_title %} ({{ main_title }}{% if parallel_series_title %} = {{ parallel_series_title }}{% endif %}{% if series_title_information %} : {{ series_title_information }}{% endif %}{% if responsibility_info %} / {{ responsibility_info }}{% endif %}{% if number %}, {{ number }}{% endif %}{% if serial_number %} ; {{ serial_number }}{% endif %}{% if sub_main_title %}. {{ sub_main_title }}{% endif %}{% if sub_parallel_series_title %} = {{ sub_parallel_series_title }}{% endif %}{% if sub_series_title_information %} : {{ sub_series_title_information }}{% endif %}{% if sub_responsibility_info %} / {{ sub_responsibility_info }}{% endif %}{% if sub_number %}, {{ sub_number }}{% endif %}{% if sub_serial_number %} ; {{ sub_serial_number }}{% endif %}){% endif %}{% if notes %}. – {{ notes }}{% endif %}{% if general_notes %}. – {{ general_notes }}{% endif %}{% if bibliography %} – Библиогр.: с. {{ bibliography }}.{% endif %}{% if isbn %} – ISBN {{ isbn }}{% endif %}{% if additional_information %} ({{ additional_information }}){% endif %}{% if fingerprint %}. – Фингерпринт: {{ fingerprint }}{% endif %}{% if availability %} : {{ availability }}{% endif %}{% if content %}. – {{ content }}{% endif %}{% if content_type %} ({{ content_type }}){% endif %}{% if access_means %} : {{ access_means }}{% endif %}',
        'authors': '''
            {% if fourth_surname or fourth_initials %}}
                {{ title }}{% if parallel %} = {{ parallel }}{% endif %} : {{ manual_type }} пособие{% if explanations %} : [{{ explanations }}]{% endif %} / {{ initials }} {{ surname }}, {{ second_initials_3 }} {{ second_surname_3 }}, {{ third_initials_2 }} {{ third_surname_2 }}, {{ fourth_initials }} {{ fourth_surname }}
            {% else %}
                {% if second_surname_4 or second_initials_4 %}
                    {{ title }}{% if parallel %} = {{ parallel }}{% endif %} : {{ manual_type }} пособие{% if explanations %} : [{{ explanations }}]{% endif %} / {{ initials }} {{ surname }}, {{ second_initials_4 }} {{ second_surname_4 }}, {{ third_initials_3 }} {{ third_surname_3 }} [и др.]
                {% else %}
                    {% if second_surname_2 or second_initials_2 %}
                        {{ surname }}, {{ initials }} {{ title }}{% if parallel %} = {{ parallel }}{% endif %} : {{ manual_type }} пособие{% if explanations %} : [{{ explanations }}]{% endif %} / {{ initials }} {{ surname }}, {{ second_initials_2 }} {{ second_surname_2 }}, {{ third_initials }} {{ third_surname }}
                    {% else %}
                        {% if second_surname or second_initials %}
                            {{ surname }}, {{ initials }} {{ title }}{% if parallel %} = {{ parallel }}{% endif %} : {{ manual_type }} пособие{% if explanations %} : [{{ explanations }}]{% endif %} / {{ initials }} {{ surname }}, {{ second_initials }} {{ second_surname }}
                        {% else %}
                            {{ surname }}, {{ initials }} {{ title }}{% if parallel %} = {{ parallel }}{% endif %} : {{ manual_type }} пособие{% if explanations %} : [{{ explanations }}]{% endif %} / {{ initials }} {{ surname }}
                        {% endif %}
                    {% endif %}
                {% endif %}
            {% endif %}
        '''
    },
    'law': { 
        'data': '{{ title }} : {{ organization }} // {{ place }}. – {{ year }}. –  № {{ publishing }}. – Ст. {{ pages }}.',
    },
    'rule': {
        'data': '{{ title }}{% if parallel %} = {{ parallel }}{% endif %}{% if type_doc %} : {{ type_doc }}{% endif %}{% if explanations %} : [{{ explanations }}]{% endif %}{% if edit_info %}. – {{ edit_info }}{% endif %}{% if par_edit_info %} = {{ par_edit_info }}{% endif %}{% if liability %} / {{ liability }}{% endif %}. – {{ place }} : {{ publishing }}, {{ year }}{% if place_of_distribution %} ; {{ place_of_distribution }}{% endif %}{% if organization_of_distribution %} : {{ organization_of_distribution }} [распространитель],{% endif %}{% if distribution_date %} {{ distribution_date }}{% endif %}{% if manufacture %} ({{ manufacture }}){% endif %}. – {{ pages }}{% if unnumbered_pages %}, [{{ unnumbered_pages }}]{% endif %} с.{% if illustrations %}, {{ illustrations }}{% endif %}{% if physical_characteristics %} : {{ physical_characteristics }}{% endif %}{% if size %} ; {{ size }} см{% endif %}{% if main_title %} ({{ main_title }}{% if parallel_series_title %} = {{ parallel_series_title }}{% endif %}{% if series_title_information %} : {{ series_title_information }}{% endif %}{% if responsibility_info %} / {{ responsibility_info }}{% endif %}{% if number %}, {{ number }}{% endif %}{% if serial_number %} ; {{ serial_number }}{% endif %}{% if sub_main_title %}. {{ sub_main_title }}{% endif %}{% if sub_parallel_series_title %} = {{ sub_parallel_series_title }}{% endif %}{% if sub_series_title_information %} : {{ sub_series_title_information }}{% endif %}{% if sub_responsibility_info %} / {{ sub_responsibility_info }}{% endif %}{% if sub_number %}, {{ sub_number }}{% endif %}{% if sub_serial_number %} ; {{ sub_serial_number }}{% endif %}){% endif %}{% if notes %}. – {{ notes }}{% endif %}{% if general_notes %}. – {{ general_notes }}{% endif %}{% if isbn %} – ISBN {{ isbn }}{% endif %}{% if accompanying %} + {{ accompanying }}{% endif %}{% if content %}. – {{ content }}{% endif %}{% if content_type %} ({{ content_type }}){% endif %}{% if access_means %} : {{ access_means }}{% endif %}',
    },
    'patent': { 
        'data': 'Патент № {{ info }}. {{ title }}{% if explanations %} : [{{ explanations }}]{% endif %} : № {{ number }} : заявл. {{ application }} : опубл. {{ publication }} / {{ author }}{% if responsibility %} ; {{ responsibility }}.{% endif %} – {{ pages }}{% if unnumbered_pages %}, [{{ unnumbered_pages }}]{% endif %} с.{% if illustrations %}, {{ illustrations }}{% endif %}{% if physical_characteristics %} : {{ physical_characteristics }}{% endif %}{% if size %} ; {{ size }} см{% endif %}{% if general_notes %}. – {{ general_notes }}{% endif %}{% if accompanying %} + {{ accompanying }}{% endif %}{% if content %}. – {{ content }}{% endif %}{% if content_type %} ({{ content_type }}){% endif %}{% if access_means %} : {{ access_means }}{% endif %}',
    },
    'sitearticle': { 
        'data': '{{ title }} // {{ site_title }} : сайт. – URL: {{ url }} (дата обращения: {{ date }})',
    }
}


class Source(models.Model):
    reference = models.TextField('Библиографическое описание', blank=True)
    list_id = models.CharField(max_length=300, default='')
    pub_date = models.CharField(max_length=100, default='')

    class Meta:
        abstract = True

    @property
    def create_description(self): # создание библиографического описания
        context = self.__dict__ # информация об источнике, введенная пользователем
        source = DESCRIPTIONS[self._meta.model_name] # схема библиографического описания для этого типа источника
        
        try: # если у этого типа источника есть поле 'url', 
            context['url'] = unquote(context['url']) # url источника декодируется для замены escape-последовательностей %xx их односимвольными эквивалентами
        except: 
            pass
        
        try: # если у этого типа источника есть поле 'date', 
            date_today = date.today().strftime('%d.%m.%Y') # в библиографическое описание вставляется текущая дата
            context['date'] = date_today
        except: 
            pass
        
        try: # если у источника есть более одного автора
            authors = source['authors']
            data = source['data']
            return Template(f'{authors}{data}').render(context)
        except: # если у источника один автор или их нет
            return Template(source['data']).render(context) 

    def __str__(self):
        return self.reference

    def save(self, *args, **kwargs):
        self.reference = self.create_description.strip().replace("\n","")
        super().save(*args, **kwargs)


class SourceWithoutAuthors(Source):
    explanations = models.CharField('Пояснения к заглавию, жанру и т.п.', max_length=300, blank=True)
    content = models.CharField('Вид содержания', max_length=300, blank=True)
    access_means = models.CharField('Средство доступа', max_length=300, blank=True)

    class Meta:
        abstract = True

class SourceWithAuthors(SourceWithoutAuthors):
    surname = models.CharField('Фамилия автора', max_length=300, blank=False, default='')
    initials = models.CharField('Инициалы автора', max_length=300, blank=False, default='')
    second_surname = models.CharField('Фамилия второго автора', max_length=300, blank=True)
    second_initials = models.CharField('Инициалы второго автора', max_length=300, blank=True)
    second_surname_2 = models.CharField('Фамилия второго автора', max_length=300, blank=True)
    second_initials_2 = models.CharField('Инициалы второго автора', max_length=300, blank=True)
    third_surname = models.CharField('Фамилия третьего автора', max_length=300, blank=True)
    third_initials = models.CharField('Инициалы третьего автора', max_length=300, blank=True)
    second_surname_3 = models.CharField('Фамилия второго автора', max_length=300, blank=True)
    second_initials_3 = models.CharField('Инициалы второго автора', max_length=300, blank=True)
    third_surname_2 = models.CharField('Фамилия третьего автора', max_length=300, blank=True)
    third_initials_2 = models.CharField('Инициалы третьего автора', max_length=300, blank=True)
    fourth_surname = models.CharField('Фамилия четвертого автора', max_length=300, blank=True)
    fourth_initials = models.CharField('Инициалы четвертого автора', max_length=300, blank=True)
    second_surname_4 = models.CharField('Фамилия второго автора', max_length=300, blank=True)
    second_initials_4 = models.CharField('Инициалы второго автора', max_length=300, blank=True)
    third_surname_3 = models.CharField('Фамилия третьего автора', max_length=300, blank=True)
    third_initials_3 = models.CharField('Инициалы третьего автора', max_length=300, blank=True)

    class Meta:
        abstract = True

class OptionalInfo(models.Model):
    edit_info = models.CharField('Сведения об издании (если указаны)', max_length=300, blank=True)
    parallel = models.CharField('Параллельное заглавие', max_length=300, blank=True)
    type_doc = models.CharField('Сведения о заглавии', max_length=300, blank=True)
    responsibility = models.CharField('Сведения об ответственности', max_length=300, blank=True)
    par_edit_info = models.CharField('Пар. сведения об издании', max_length=300, blank=True)
    liability = models.CharField('Свед. об отв-ти, относ. к изданию', max_length=300, blank=True)
    place_of_distribution = models.CharField('Место распространения', max_length=300, blank=True)
    organization_of_distribution = models.CharField('Организация распространения', max_length=300, blank=True)
    distribution_date = models.CharField('Дата распространения', max_length=300, blank=True)
    manufacture = models.CharField('Сведения об изготовлении', max_length=300, blank=True)
    unnumbered_pages = models.CharField('Ненумерованные страницы', max_length=300, blank=True)
    illustrations = models.CharField('Ненумерованные листы, столбцы', max_length=300, blank=True)
    accompanying = models.CharField('Сопроводительный материал', max_length=300, blank=True)
    notes = models.CharField('Примечания', max_length=300, blank=True)
    general_notes = models.CharField('Примечания общего характера', max_length=300, blank=True)
    additional_information = models.CharField('Доп. свед-я идентификатора ресурса', max_length=300, blank=True)
    availability = models.CharField('Условия доступности', max_length=300, blank=True)
    content_type = models.CharField('Характеристика содержания', max_length=300, blank=True)

    class Meta:
        abstract = True

class SeriesInfo(models.Model):
    main_title = models.CharField('Основное заглавие серии', max_length=300, blank=True)
    parallel_series_title = models.CharField('Параллельное заглавие серии', max_length=300, blank=True)
    series_title_information = models.CharField('Свед-я, относ. к заглавию серии', max_length=300, blank=True)
    responsibility_info = models.CharField('Свед-я об отв-ти, относ. к серии', max_length=300, blank=True)
    number = models.CharField('Междунар. станд. номер серии', max_length=300, blank=True)
    serial_number = models.CharField('Номер выпуска серии', max_length=300, blank=True)
    sub_main_title = models.CharField('Основное заглавие подсерии', max_length=300, blank=True)
    sub_parallel_series_title = models.CharField('Пар. заглавие подсерии', max_length=300, blank=True)
    sub_series_title_information = models.CharField('Свед-я, относ. к заглавию подсерии', max_length=300, blank=True)
    sub_responsibility_info = models.CharField('Свед-я об отв-ти, относ. к подсерии', max_length=300, blank=True)
    sub_number = models.CharField('Междунар. станд. номер подсерии', max_length=300, blank=True)
    sub_serial_number = models.CharField('Номер выпуска подсерии', max_length=300, blank=True)

    class Meta:
        abstract = True


class Publication(SourceWithAuthors, OptionalInfo, SeriesInfo):
    class Meta:
        abstract = True


class Book(Publication):
    title = models.CharField('Название книги', max_length=300, blank=False)
    place = models.CharField('Место издания', max_length=300, blank=False)
    publishing = models.CharField('Издательство', max_length=300, blank=False)
    year = models.CharField('Год издания книги', max_length=300, blank=False)
    pages = models.CharField('Количество страниц', max_length=300, blank=False)
    isbn = models.CharField('ISBN (если указан)', max_length=300, blank=True)
    fingerprint = models.CharField('Фингерпринт (для старопеч. изд.)', max_length=300, blank=True)
    size = models.CharField('Размер издания (в см)', max_length=300, blank=True)
    physical_characteristics = models.CharField('Физические характеристики', max_length=300, blank=True)

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
