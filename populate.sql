
INSERT INTO `papel` (`id`, `descricao`) VALUES
(null, 'Administrador'),
(null, 'Professor');


INSERT INTO `usuario` (`id`, `email`, `nome`, `senha_hash`, `denominacao`, `papel_id`, `is_admin`) VALUES
(null, 'lucao_soares@hotmail.com', 'Lucas Soares', 'pbkdf2:sha1:1000$afGU9OcM$93524cee1548bbf329de84d09481bb7266e465fd', 'Desenvolvedor', 2, 1),
(null, 's@a.com', 'Sakaue', 'pbkdf2:sha1:1000$cY6k29ev$94276419b0bd77fea420e3b3ea6d0221683f5e3a', 'Professor', 1, 0),
(null, 'william.menezes@fatec.sp.gov.br', 'William M M Menezes', 'pbkdf2:sha1:1000$hOSdf9GY$dc97cee1df17b440e850969a6b40757f8ae6678d', 'Doutor', 2, 1);



INSERT INTO `laboratorio` (`id`, `descricao`, `auditado`, `professorTitular_id`, `professorSuplente_id`) VALUES
(null, 'Instrumentação aplicada', 0, 1, 2),
(null, 'Reagentes e polímeros', 0, 3, 2),
(null, 'Metrologia', 0, 3, 1),
(null, 'Recepção de projetos', 0, 3, 2);

INSERT INTO `insumo` (`id`, `descricao`, `quantidadeAtual`, `quantidadeMinima`, `laboratorio_id`) VALUES 
(NULL, 'Reagente A', '10', '5', '2'), 
(NULL, 'Reagente B', '10', '15', '2'), 
(NULL, 'Polímero', '10', '10', '2');
