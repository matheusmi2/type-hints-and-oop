class ZoologicoErro(Exception):
    pass


class EntidadeNaoEncontradaErro(ZoologicoErro):
    pass


class EntidadeJaExisteErro(ZoologicoErro):
    pass


class CapacidadeRecintoErro(ZoologicoErro):
    pass


class OperacaoInvalidaErro(ZoologicoErro):
    pass
