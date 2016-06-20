# -*- coding: utf-8
from __future__ import unicode_literals
from prompt_toolkit.filters import Condition
from prompt_toolkit.enums import DEFAULT_BUFFER, SEARCH_BUFFER
from prompt_toolkit.filters import IsDone, HasFocus, RendererHeightIsKnown, to_cli_filter
from prompt_toolkit.layout import Window, HSplit, FloatContainer, Float
from prompt_toolkit.layout.containers import ConditionalContainer
from prompt_toolkit.layout.controls import BufferControl, TokenListControl, FillControl
from prompt_toolkit.layout.dimension import LayoutDimension as D
from prompt_toolkit.layout.lexers import PygmentsLexer
from prompt_toolkit.layout.margins import PromptMargin, ConditionalMargin
from prompt_toolkit.layout.menus import CompletionsMenu, MultiColumnCompletionsMenu
from prompt_toolkit.layout.processors import PasswordProcessor, ConditionalProcessor, AppendAutoSuggestion, HighlightSearchProcessor, HighlightSelectionProcessor
from prompt_toolkit.layout.prompt import DefaultPrompt
from prompt_toolkit.layout.screen import Char
from prompt_toolkit.layout.toolbars import ValidationToolbar, SystemToolbar, ArgToolbar, SearchToolbar
from prompt_toolkit.token import Token
from prompt_toolkit.shortcuts import _split_multiline_prompt, _RPrompt

from six import text_type

try:
    from pygments.lexer import Lexer as pygments_Lexer
    from pygments.style import Style as pygments_Style
except ImportError:
    pygments_Lexer = None
    pygments_Style = None


def create_prompt_layout(message='',
                         lexer=None,
                         is_password=False,
                         reserve_space_for_menu=8,
                         get_prompt_tokens=None,
                         get_continuation_tokens=None,
                         get_rprompt_tokens=None,
                         get_bottom_toolbar_tokens=None,
                         display_completions_in_columns=False,
                         extra_input_processors=None,
                         get_panels_on=None,
                         multiline=False,
                         wrap_lines=True):
    """
    Create a :class:`.Container` instance for a prompt.

    :param message: Text to be used as prompt.
    :param lexer: :class:`~prompt_toolkit.layout.lexers.Lexer` to be used for
        the highlighting.
    :param is_password: `bool` or :class:`~prompt_toolkit.filters.CLIFilter`.
        When True, display input as '*'.
    :param reserve_space_for_menu: Space to be reserved for the menu. When >0,
        make sure that a minimal height is allocated in the terminal, in order
        to display the completion menu.
    :param get_prompt_tokens: An optional callable that returns the tokens to be
        shown in the menu. (To be used instead of a `message`.)
    :param get_continuation_tokens: An optional callable that takes a
        CommandLineInterface and width as input and returns a list of (Token,
        text) tuples to be used for the continuation.
    :param get_bottom_toolbar_tokens: An optional callable that returns the
        tokens for a toolbar at the bottom.
    :param display_completions_in_columns: `bool` or
        :class:`~prompt_toolkit.filters.CLIFilter`. Display the completions in
        multiple columns.
    :param multiline: `bool` or :class:`~prompt_toolkit.filters.CLIFilter`.
        When True, prefer a layout that is more adapted for multiline input.
        Text after newlines is automatically indented, and search/arg input is
        shown below the input, instead of replacing the prompt.
    :param wrap_lines: `bool` or :class:`~prompt_toolkit.filters.CLIFilter`.
        When True (the default), automatically wrap long lines instead of
        scrolling horizontally.
    """
    assert isinstance(message, text_type), 'Please provide a unicode string.'
    assert get_bottom_toolbar_tokens is None or callable(get_bottom_toolbar_tokens)
    assert get_prompt_tokens is None or callable(get_prompt_tokens)
    assert get_rprompt_tokens is None or callable(get_rprompt_tokens)
    assert not (message and get_prompt_tokens)

    display_completions_in_columns = to_cli_filter(display_completions_in_columns)
    multiline = to_cli_filter(multiline)

    if get_prompt_tokens is None:
        get_prompt_tokens = lambda _: [(Token.Prompt, message)]

    get_prompt_tokens_1, get_prompt_tokens_2 = _split_multiline_prompt(get_prompt_tokens)

    # `lexer` is supposed to be a `Lexer` instance. But if a Pygments lexer
    # class is given, turn it into a PygmentsLexer. (Important for
    # backwards-compatibility.)
    try:
        if pygments_Lexer and issubclass(lexer, pygments_Lexer):
            lexer = PygmentsLexer(lexer, sync_from_start=True)
    except TypeError:  # Happens when lexer is `None` or an instance of something else.
        pass

    # Create processors list.
    input_processors = [
        ConditionalProcessor(
            # By default, only highlight search when the search
            # input has the focus. (Note that this doesn't mean
            # there is no search: the Vi 'n' binding for instance
            # still allows to jump to the next match in
            # navigation mode.)
            HighlightSearchProcessor(preview_search=True),
            HasFocus(SEARCH_BUFFER)),
        HighlightSelectionProcessor(),
        ConditionalProcessor(AppendAutoSuggestion(), HasFocus(DEFAULT_BUFFER) & ~IsDone()),
        ConditionalProcessor(PasswordProcessor(), is_password)
    ]

    if extra_input_processors:
        input_processors.extend(extra_input_processors)

    # Show the prompt before the input (using the DefaultPrompt processor.
    # This also replaces it with reverse-i-search and 'arg' when required.
    # (Only for single line mode.)
    # (DefaultPrompt should always be at the end of the processors.)
    input_processors.append(ConditionalProcessor(
        DefaultPrompt(get_prompt_tokens_2), ~multiline))

    # Create bottom toolbar.
    if get_bottom_toolbar_tokens:
        toolbars = [ConditionalContainer(
            Window(TokenListControl(get_bottom_toolbar_tokens,
                                    default_char=Char(' ', Token.Toolbar)),
                   height=D.exact(1)),
            filter=~IsDone() & RendererHeightIsKnown())]
    else:
        toolbars = []

    def get_height(cli):
        # If there is an autocompletion menu to be shown, make sure that our
        # layout has at least a minimal height in order to display it.
        if reserve_space_for_menu and not cli.is_done:
            buff = cli.current_buffer

            # Reserve the space, either when there are completions, or when
            # `complete_while_typing` is true and we expect completions very
            # soon.
            if buff.complete_while_typing(cli) or buff.complete_state is not None:
                return D(min=reserve_space_for_menu)

        return D()

    show_panels = Condition(lambda cli: get_panels_on())

    buffer_window = Window(
        BufferControl(
            input_processors=input_processors,
            lexer=lexer,
            # Enable preview_search, we want to have immediate feedback
            # in reverse-i-search mode.
            preview_search=True),
        get_height=get_height,
        left_margins=[
            # In multiline mode, use the window margin to display
            # the prompt and continuation tokens.
            ConditionalMargin(
                PromptMargin(get_prompt_tokens_2, get_continuation_tokens),
                filter=multiline
            )
        ],
        wrap_lines=wrap_lines
    )

    tokens_window = ConditionalContainer(
        Window(
            TokenListControl(get_prompt_tokens_1),
            dont_extend_height=True),
        ~show_panels
    )

    info_window = ConditionalContainer(
        Window(FillControl('P', Token.Line)),
        show_panels
    )

    completion_float = Float(
        xcursor=True,
        ycursor=True,
        content=CompletionsMenu(
            max_height=16,
            scroll_offset=1,
            extra_filter=HasFocus(DEFAULT_BUFFER) &
                         ~display_completions_in_columns))

    completion_multi_float = Float(
        xcursor=True,
        ycursor=True,
        content=MultiColumnCompletionsMenu(
          extra_filter=HasFocus(DEFAULT_BUFFER) &
                       display_completions_in_columns,
          show_meta=True))

    # The right prompt.
    right_prompt_float = Float(right=0, top=0, hide_when_covering_content=True,
                               content=_RPrompt(get_rprompt_tokens)),

    # Create and return Container instance.
    return HSplit([
          # The main input, with completion menus floating on top of it.
          FloatContainer(
              HSplit([
                  info_window,
                  tokens_window,
                  buffer_window,
              ]),
              [
                  # Completion menus.
                  completion_float,
                  completion_multi_float,
                  right_prompt_float
              ]
          ),
          ValidationToolbar(),
          SystemToolbar(),

          # In multiline mode, we use two toolbars for 'arg' and 'search'.
          ConditionalContainer(ArgToolbar(), multiline),
          ConditionalContainer(SearchToolbar(), multiline),
      ] + toolbars)
