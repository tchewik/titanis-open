from collections import namedtuple
from time import time
from typing import *

from .features import *

__all__ = (
    'up_modules',
    'ModuleManager',
    'AVAILABLE_MODULES',
    'Endpoint',
    'Module',
    'UDPipe',
    'Mystem',
    'PsyCues',
    'PsyDict',
    'Syntax',
    'Frustration',
    'Discourse'
)

Dependency = namedtuple('Dependency', ['module', 'data_name'])


class ModuleData(dict):
    def is_available(self) -> bool:
        return len(self) > 0


class Module:
    def __init__(
            self, name: str,
            extractor_cls: Type[BaseFeaturesExtractor],
            dependencies: List[Union[Dependency]]):
        self.name = name
        self.dependencies = dependencies
        self._extractor_cls = extractor_cls
        self._extractor = None
        self._elapsed_time = False
        self._is_host_required = issubclass(self._extractor_cls, BaseDockerExtractor)

    def up(self, host, elapsed_time, **kwargs):
        self._elapsed_time = elapsed_time
        if self.is_host_required():
            self._extractor = self._extractor_cls(host, **kwargs)
        else:
            self._extractor = self._extractor_cls(**kwargs)

    def __call__(self, *args, **kwargs) -> ModuleData:
        if self._elapsed_time:
            start_time = time()
            extractor_out = self._extractor(*args, **kwargs)
            extractor_out['result_time'] = time() - start_time
            return ModuleData(**extractor_out)
        else:
            return ModuleData(**self._extractor(*args, **kwargs))

    def is_host_required(self):
        return self._is_host_required

    def is_upped(self):
        return bool(self._extractor)

    def is_elapsed_time(self):
        return self._elapsed_time


Endpoint = Module(
    name='Endpoint',
    extractor_cls=DummyFeaturesExtractor,
    dependencies=[]
)

UDPipe = Module(
    name='UDPipe',
    extractor_cls=FeaturesUDPipe,
    dependencies=[Dependency(Endpoint, 'text')]
)

Mystem = Module(
    name='Mystem',
    extractor_cls=FeaturesMystem,
    dependencies=[
        Dependency(UDPipe, 'tokens'),
        Dependency(UDPipe, 'sentences')
    ]
)

SRL = Module(
    name='SRL',
    extractor_cls=FeaturesSRL,
    dependencies=[
        Dependency(UDPipe, 'tokens'),
        Dependency(Mystem, 'postag_mys'),
        Dependency(Mystem, 'morph_mys'),
        Dependency(UDPipe, 'lemma_udp'),
        Dependency(UDPipe, 'syntax_dep_tree_udp')
    ]
)

RST = Module(
    name='RST',
    extractor_cls=FeaturesRST,
    dependencies=[
        Dependency(Endpoint, 'text'),
        Dependency(UDPipe, 'tokens'),
        Dependency(UDPipe, 'sentences'),
        Dependency(Mystem, 'postag_mys'),
        Dependency(Mystem, 'morph_mys'),
        Dependency(UDPipe, 'lemma_udp'),
        Dependency(UDPipe, 'syntax_dep_tree_udp')
    ]
)

PsyCues = Module(
    name='PsyCues',
    extractor_cls=FeaturesPsyCues,
    dependencies=[(Endpoint, 'text'),
                  (Mystem, 'lemma_mys'),
                  (Mystem, 'postag_mys_unconverted')]
)

PsyDict = Module(
    name='PsyDict',
    extractor_cls=FeaturesPsyDict,
    dependencies=[(Mystem, 'lemma_mys')]
)

Syntax = Module(
    name='Syntax',
    extractor_cls=FeaturesSyntax,
    dependencies=[Dependency(UDPipe, 'syntax_dep_tree_udp')]
)

Frustration = Module(
    name='Frustration',
    extractor_cls=ClassifierFrustration,
    dependencies=[Dependency(Endpoint, 'text')]
)

Discourse = Module(
    name='Discourse',
    extractor_cls=FeaturesDiscourse,
    dependencies=[Dependency(RST, 'rst')]
)

AVAILABLE_MODULES = (
    UDPipe,
    Mystem,
    SRL,
    RST,
    PsyCues,
    PsyDict,
    Syntax,
    Frustration,
    Discourse,
)


class ModuleManager:
    def __init__(self, host: str, required_module_list: List[Module]):
        self.host = host
        self.required_module_list = required_module_list
        self._module_data = {module: ModuleData() for module in AVAILABLE_MODULES}

    def __call__(self, text):
        self._module_data[Endpoint] = Endpoint(text)
        for module in self.required_module_list:
            self._run_rec(module)
        return self._get_returned_data()

    def _run_rec(self, module):
        if not self._module_data[module].is_available():
            args = []
            for dependency_module, data_name in module.dependencies:
                self._run_rec(dependency_module)
                if data_name == 'all':
                    args.append(self._get_all_module_variables(dependency_module))
                else:
                    args.append(self._module_data[dependency_module][data_name])
            self._module_data[module] = module(*args)

    def _get_returned_data(self):
        returned_module_data = {}
        for module, module_data in self._module_data.items():
            if module is not Endpoint:
                returned_module_data[module.name] = module_data
        return returned_module_data

    def _get_all_module_variables(self, module):
        if module.is_elapsed_time():
            data = self._module_data[module].copy()
            del data['result_time']
            return data
        else:
            return self._module_data[module]


def up_modules(host, modules_args, required_modules, elapsed_time):
    Endpoint.up(host, elapsed_time=False)  # required module for all runs
    for module in required_modules:
        _up_rec(module, host, modules_args, elapsed_time)


def _up_rec(module, host, modules_args, elapsed_time):
    if not module.is_upped():
        module.up(host, elapsed_time, **modules_args.get(module, {}))
        for dependency_module, _ in module.dependencies:
            _up_rec(dependency_module, host, modules_args, elapsed_time)
