import typing
from .modules import AVAILABLE_MODULES, ModuleManager, Module, up_modules, PsyCues, PsyDict, RST


class Titanis:

    def __init__(
            self, host='172.17.0.1',
            # main modules
            psy_cues=False, psy_dict=False, syntax=False, frustration_clf=False, discourse=False,
            # additional args
            psy_cues_normalization='words', psy_dict_normalization='words',
            elapsed_time=False,
            # 0-level analyzers modules
            udpipe=False, mystem=False, srl=False, rst=False, emotive_srl=False,
    ):
        """ Pass host = 'remote.server.ru' to run Titanis in remote server
            if required_modules not passed, ups all available modules """
        self.host = host
        self._create_required_module_list(udpipe, mystem, srl, rst, psy_cues, psy_dict, syntax, frustration_clf,
                                          discourse, emotive_srl)
        modules_args = {
            PsyCues: {'psy_cues_normalization': psy_cues_normalization},
            PsyDict: {'psy_dict_normalization': psy_dict_normalization},
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
                                     discourse, emotive_srl):
        self.required_module_list = []
        for module_is_required, module in zip(
                (udpipe, mystem, srl, rst, psy_cues, psy_dict, syntax, frustration_clf, discourse, emotive_srl),
                AVAILABLE_MODULES
        ):
            if module_is_required:
                self.required_module_list.append(module)
        if not self.required_module_list:
            self.required_module_list = AVAILABLE_MODULES
