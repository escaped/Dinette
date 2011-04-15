from django import  template
from django.contrib.sites.models import Site

from dinette.models import Ftopics, SiteConfig, NavLink

register = template.Library()

class BaseDinetteNode(template.Node):
    @classmethod
    def handle_token(cls, parser, token):
        tokens = token.contents.split()
        if len(tokens) == 3:
            if tokens[1] != "as":
                 raise template.TemplateSyntaxError("Second argument in %r must be 'as'" % tokens[0])
            return cls(
                        as_varname=tokens[2]
                        )
        else:
            return cls()

class GetAnnouncementNode(BaseDinetteNode):
    def __init__(self, as_varname='announcement'):
        self.as_varname = as_varname

    def render(self, context):
        try:
            ancount = Ftopics.objects.filter(announcement_flag=True).count()
            if(ancount > 0):
                announcement = Ftopics.objects.filter(announcement_flag=True).latest()
                context[self.as_varname] = announcement
                return ''
        except Ftopics.DoesNotExist:
            return ''

@register.tag
def get_announcement(parser, token):
    return GetAnnouncementNode.handle_token(parser, token)

class GetNavLinksNode(BaseDinetteNode):
    def __init__(self, as_varname='nav_links'):
        self.as_varname = as_varname

    def render(self, context):
        context[self.as_varname] = NavLink.objects.all()
        return ''

@register.tag
def get_forumwide_links(parser, token):
    return GetNavLinksNode.handle_token(parser, token)

@register.simple_tag
def get_site_name():
    try:
        config = SiteConfig.objects.get(id=1)
        return config.name
    except SiteConfig.DoesNotExist:
        return ''

@register.simple_tag
def get_site_tag_line():
    try:
        config = SiteConfig.objects.get(id=1)
        return config.tag_line
    except SiteConfig.DoesNotExist:
        return ''
    
@register.simple_tag
def get_main_site_name():
    try:
        name = Site.objects.get_current().name
        return name
    except:
        return ''

@register.simple_tag
def get_main_site_domain():
    try:
        domain = Site.objects.get_current().domain
        return domain
    except:
        return ''

# http://od-eon.com/blogs/liviu/django-urlize-html-safe/
from django.utils.html import urlize
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
def html_urlize(value, autoescape=None):
    """Converts URLs in plain text into clickable links."""
    from BeautifulSoup import BeautifulSoup
    ignored_tags = ['a', 'code', 'pre']
    soup = BeautifulSoup(value)
    tags = soup.findAll(True)
    text_all = soup.contents
    for text in text_all:
        if text not in tags:
            parsed_text = urlize(text, nofollow=True, autoescape=autoescape)
            text.replaceWith(parsed_text)
    for tag in tags:
        if not tag.name in ignored_tags:
            soup_text = BeautifulSoup(str(tag))
            if len(soup_text.findAll()) > 1:
                for child_tag in tag.contents:
                    child_tag.replaceWith(html_urlize(str(child_tag)))
            elif len(soup_text.findAll()) > 0:
                text_list = soup_text.findAll(text=True)
                for text in text_list:
                    parsed_text = urlize(text, nofollow=True, autoescape=autoescape)
                    text.replaceWith(parsed_text)
                try:
                    tag.replaceWith(str(soup_text))
                except:
                    pass
    return mark_safe(str(soup))
html_urlize.is_safe = True
html_urlize.needs_autoescape = True
html_urlize = stringfilter(html_urlize)
register.filter(html_urlize)