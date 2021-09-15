import typing
from .modules import AVAILABLE_MODULES, ModuleManager, Module, up_modules, PsyCues, PsyDict, RST


class Titanis:

    def __init__(
            self, host='172.17.0.1',
            # main modules
            psy_cues=False, psy_dict=False, syntax=False, frustration_clf=False, discourse=False,
            rosenzweig=False, depression_clf=False,
            # additional args
            psy_cues_normalization='words', psy_dict_normalization='words', discourse_long_text_only=False,
            elapsed_time=False,
            # 0-level analyzers modules
            udpipe=False, mystem=False, srl=False, rst=False
    ):
        """ Pass host = 'remote.server.ru' to run Titanis in remote server
            if required_modules not passed, ups all available modules """
        self.host = host
        self._create_required_module_list(udpipe, mystem, srl, rst, psy_cues, psy_dict, syntax, frustration_clf,
                                          discourse, rosenzweig, depression_clf)
        modules_args = {
            PsyCues: {'psy_cues_normalization': psy_cues_normalization},
            PsyDict: {'psy_dict_normalization': psy_dict_normalization},
            RST: {'discourse_long_text_only': discourse_long_text_only}
        }
        up_modules(self.host, modules_args, self.required_module_list, elapsed_time)

    def __call__(
            self, text: str,
    ) -> typing.Union[Module, typing.List[Module]]:
        # create modules pipeline
        module_manager = ModuleManager(self.host, self.required_module_list)
        # process text
        return module_manager(text)

    def _create_required_module_list(self, udpipe, mystem, srl, rst, psy_cues, psy_dict, syntax, frustration_clf,
                                     discourse):
        self.required_module_list = []
        for module_is_required, module in zip(
                (udpipe, mystem, srl, rst, psy_cues, psy_dict, syntax, frustration_clf, discourse),
                AVAILABLE_MODULES
        ):
            if module_is_required:
                self.required_module_list.append(module)
        if not self.required_module_list:
            self.required_module_list = AVAILABLE_MODULES
