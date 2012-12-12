
from ist.transform import BaseTransformer
import ist.ist_types as it


class SemantifyTransformer(BaseTransformer):
	"""sematification (SemantifyTransformer) > making sure python's semantics (functions, classes, errorhandling)"""
	
	def trans_Module(self, node):
		return it.Module('test', [it.Call(
			func  = it.Name('PY$Module', it.Load()),
			args = [
				it.FunctionDef(
					name = None,
					args = [it.Name('mod', it.Param())],
					body = node.body,
					decorator_list = []
				)
			],
			keywords = [],
			starargs = None,
			kwargs = None
		)])

	def trans_Print(self, node):
		assert node.dest == None

		return it.Call(
			func  = it.Name('print', it.Load()),
			args = node.values,
			keywords = [],
			starargs = None,
			kwargs = None
		)