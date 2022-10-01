# Keypirinha launcher (keypirinha.com)

import keypirinha as kp
import keypirinha_util as kpu
import keypirinha_net as kpnet
import os.path
import os

from collections import namedtuple
import datetime


AnswerTuple = namedtuple('AnswerTuple', ('value', 'datetime'))

class DevDocs(kp.Plugin):
    """
    Search the DevDocs API documentation.

    This block is a longer and more detailed description of your plugin that may
    span on several lines, albeit not being required by the application.

    You may have several plugins defined in this module. It can be useful to
    logically separate the features of your package. All your plugin classes
    will be instantiated by Keypirinha as long as they are derived directly or
    indirectly from :py:class:`keypirinha.Plugin` (aliased ``kp.Plugin`` here).

    In case you want to have a base class for your plugins, you must prefix its
    name with an underscore (``_``) to indicate Keypirinha it is not meant to be
    instantiated directly.

    In rare cases, you may need an even more powerful way of telling Keypirinha
    what classes to instantiate: the ``__keypirinha_plugins__`` global variable
    may be declared in this module. It can be either an iterable of class
    objects derived from :py:class:`keypirinha.Plugin`; or, even more dynamic,
    it can be a callable that returns an iterable of class objects. Check out
    the ``StressTest`` example from the SDK for an example.

    Up to 100 plugins are supported per module.

    Search for the "DevDocs" prefix to check what sites are already in the
    Catalog. Additional search sites can be added in package's configuration file.
    """

    # FIXME: Should be removed
    _debug = True

    CONFIG_SECTION_MAIN = "main"
    CONFIG_SECTION_ENV = "env"

    SUPPORTED_CACHE_METHOD = ["onstart", "off"]
    SUPPORTED_TITLE_LEVEL = ["firstlevel", "secondlevel"]
    SUPPORTED_COPY_FROM_CLIPBOARD = False

    DEFAULT_ITEM_LABEL_FORMAT = "DevDocs"
    DEFAULT_CACHE_METHOD = "onstart"
    DEFAULT_CACHE_LEVEL = "firstlevel"
    DEFAULT_COPY_FROM_CLIPBOARD = False
    DEFAULT_COPY_FROM_CLIPBOARD_TO = "secondlevel"
    DEFAULT_INCLUDE_DOCUMENTATION = []
    DEFAULT_EXCLUDE_DOCUMENTATION = []

    ITEMCAT_RESULT = kp.ItemCategory.USER_BASE + 1

    default_icon_handle = None
    history = []

    def __init__(self):
        super().__init__()

    def on_start(self):
        self.info("Loading DevDocs Package (Start Up)")
        self._setup_default_icon()
        # Read configuration
        self._load_config()
        # Set Actions
        # 1. Open URL in browser
        # 2. Open URL in browser using Incognito
        self.set_actions(self.ITEMCAT_RESULT, [
                             self.create_action(
                                 name = "copy",
                                 label = "Copy",
                                 short_desc = "Copy the name of the answer")
                         ])

    def on_catalog(self):
        # Change to DevDocs Icon
        self._setup_default_icon()
        # Load up available documentation
        self.set_catalog([self.create_item(
            category = kp.ItemCategory.KEYWORD,
            label = "DevDocs",
            short_desc = "Search DevDocs API documentation(s)",
            target="devdocs",
            args_hint = kp.ItemArgsHint.REQUIRED,
            hit_hint = kp.ItemHitHint.NOARGS)])
        self.info("Catalog Done")

    def on_suggest(self, user_input, items_chain):
        if not items_chain or items_chain[-1].category() != kp.ItemCategory.KEYWORD:
            return

        self.dbg("user-input: {}".format(user_input));

        for item in items_chain:
            self.dbg("Listing Items Chain")
            self.dbg([
                         item.label(),
                         item.short_desc()
                     ])

        if not user_input:
            self.history = []

        # Generate a new answer
        ans = AnswerTuple(
            os.urandom(1)[0] % 2,
            datetime.datetime.now()
        )
        self.dbg(ans)
        self.history.append(ans)

        suggestions = []
        for idx in range(len(self.history) - 1, -1, -1):
            answer = self.history[idx]
            desc = "{}, {} (press Enter to copy)".format(
                idx + 1, answer.datetime.strftime("%H:%M:%S")
            )
            suggestions.append(self.create_item(
                                   category = self.ITEMCAT_RESULT,
                                   label = self._value_to_string(answer.value),
                                   short_desc = desc,
                                   target = "{},{}".format(answer.value, idx),
                                   args_hint=kp.ItemArgsHint.FORBIDDEN,
                                   hit_hint=kp.ItemHitHint.IGNORE
                               ))
            self.set_suggestions(suggestions, kp.Match.ANY, kp.Sort.NONE)

    def on_execute(self, item, action):
        self.dbg([
                     item,
                     action
                 ])
        if item and item.category() == self.ITEMCAT_RESULT:
            value = int(item.target().split(',', maxsplit=1)[0])
            kpu.set_clipboard(self._value_to_string(value))

    def on_activated(self):
        pass

    def on_deactivated(self):
        pass

    def on_events(self, flags):
        self.log("Loading DevDocs Package")
        pass

    def _value_to_string(self, value):
        return "Yes" if value else "No"

    # TODO: [For Future, another method] _load_icons(self)?
    #       Should load *.png resources and store them for each language
    #       Should also have a default icon for DevDocs.
    # HINT: Can take icons from the freecodecamp devdocs repo
    def _setup_default_icon(self):
        if self.default_icon_handle:
            self.default_icon_handle.free()
            self.default_icon_handle = None

        ico_resource = "res://{}/devdocs.png".format(self.package_full_name())
        self.default_icon_handle = self.load_icon(ico_resource)
        if self.default_icon_handle:
            self.set_default_icon(self.default_icon_handle)

    def _load_config(self):
        settings = self.load_settings()
        cache_method: str = settings.get_stripped(
            "cache_method",
            section = self.CONFIG_SECTION_MAIN,
            fallback = self.DEFAULT_CACHE_METHOD
        )
        cache_level: str = settings.get_stripped(
            "cache_level",
            section = self.CONFIG_SECTION_MAIN,
            fallback = self.DEFAULT_CACHE_LEVEL
        )
        copy_from_clipboard: str = settings.get_bool(
            "copy_from_clipboard",
            section = self.CONFIG_SECTION_MAIN,
            fallback = self.DEFAULT_COPY_FROM_CLIPBOARD
        )

        # LOGGING
        self.dbg([
                     cache_level,
                     cache_method,
                     copy_from_clipboard
                 ])

