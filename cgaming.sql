-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 04-07-2021 a las 02:19:50
-- Versión del servidor: 10.3.29-MariaDB-0+deb10u1
-- Versión de PHP: 7.3.27-1~deb10u1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `cgaming`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `consolas`
--

CREATE TABLE `consolas` (
  `id_consola` int(11) NOT NULL,
  `nombre_cons` varchar(30) NOT NULL,
  `descripcion_cons` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `consolas`
--

INSERT INTO `consolas` (`id_consola`, `nombre_cons`, `descripcion_cons`) VALUES
(1, 'PlayStation', 'Primera consola de Sony lanzada en 1994. Se considera la más exitosa de la quinta generación.'),
(2, 'Game Boy', 'Videoconsola portátil lanzada en 1989. Es la primera de la serie Game Boy. '),
(3, 'Game Boy Advance', 'Fabricada desde 2001 hasta 2008 por la compañia Nintendo.');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `desarrolladoras`
--

CREATE TABLE `desarrolladoras` (
  `id_desarrolladora` int(11) NOT NULL,
  `nombre_desa` varchar(25) NOT NULL,
  `descripcion_desa` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `desarrolladoras`
--

INSERT INTO `desarrolladoras` (`id_desarrolladora`, `nombre_desa`, `descripcion_desa`) VALUES
(1, 'Game Freak', 'Empresa Japonesa desarrolladora de videojuegos. '),
(2, 'Konami', 'Empresa desarrolladora fundada en 1969. Actualmente tiene su base en Tokio.'),
(3, 'Atari', 'Actualmente propiedad de Atari Interactive.');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `generos`
--

CREATE TABLE `generos` (
  `id_genero` int(11) NOT NULL,
  `nombre_gen` varchar(25) NOT NULL,
  `descripcion_gen` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `generos`
--

INSERT INTO `generos` (`id_genero`, `nombre_gen`, `descripcion_gen`) VALUES
(1, 'RPG', 'Role Playing Game o juego de Rol, donde el jugador controla las acciones de un personaje o grupo de personajes.'),
(2, 'Acción', 'Avanzar a través de niveles, eliminando hordas de enemigos.'),
(3, 'Beat em up', 'Ofrece combate cuerpo a cuerpo entre el protagonista y un numero improbable de oponentes.');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `idiomas`
--

CREATE TABLE `idiomas` (
  `id_idioma` int(11) NOT NULL,
  `nombre_idioma` varchar(25) NOT NULL,
  `descripcion_idioma` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `idiomas`
--

INSERT INTO `idiomas` (`id_idioma`, `nombre_idioma`, `descripcion_idioma`) VALUES
(1, 'Inglés', 'El idioma más hablado del mundo, con mas de mil millones de personas que lo tienen como primera o segunda lengua.'),
(2, 'Español', 'Esta lengua es hablada principalmente en España e Hispanoamérica.'),
(3, 'Japonés', 'Idioma de Asia Oriental hablado principalmente en Japón, donde es la lengua oficial.');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `juegos`
--

CREATE TABLE `juegos` (
  `id_juego` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `descripcion` varchar(250) NOT NULL,
  `precio` float NOT NULL,
  `foto` varchar(150) NOT NULL,
  `foto_dos` varchar(150) NOT NULL,
  `lanzamiento` varchar(5) NOT NULL,
  `stock` int(11) NOT NULL,
  `id_consola` int(11) NOT NULL,
  `id_desarrolladora` int(11) NOT NULL,
  `id_region` int(11) NOT NULL,
  `id_genero` int(11) NOT NULL,
  `id_idioma` int(11) NOT NULL,
  `estado` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `juegos`
--

INSERT INTO `juegos` (`id_juego`, `nombre`, `descripcion`, `precio`, `foto`, `foto_dos`, `lanzamiento`, `stock`, `id_consola`, `id_desarrolladora`, `id_region`, `id_genero`, `id_idioma`, `estado`) VALUES
(1, 'Pokemon Rojo', 'Versión Roja del primer juego de Pokemon, incluye caja.', 500, '4-7-2021-2-10-17-foto-01.jpg', '4-7-2021-2-10-17-foto-02.jpg', '1998', 1, 2, 1, 3, 1, 1, 1),
(2, 'Driv3r', 'Tercera parte de la saga Driv3r. Sin caja.', 350, '4-7-2021-2-11-34-foto-01.jpg', '4-7-2021-2-11-34-foto-02.jpg', '2004', 1, 3, 3, 3, 2, 1, 1),
(3, 'TMNT II: Back from the S.', 'Secuela del primer juego Fall of the Foot Clan.', 550, '4-7-2021-2-14-41-foto-01.jpg', '4-7-2021-2-14-41-foto-02.jpg', '1991', 1, 2, 2, 3, 3, 1, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `regiones`
--

CREATE TABLE `regiones` (
  `id_region` int(11) NOT NULL,
  `nombre_reg` varchar(10) NOT NULL,
  `descripcion_reg` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `regiones`
--

INSERT INTO `regiones` (`id_region`, `nombre_reg`, `descripcion_reg`) VALUES
(1, 'PAL', 'Se utiliza en la mayoría de los países africanos, asiáticos y europeos, además de Australia y algunos países sudamericanos.'),
(2, 'NTSC', 'Se utiliza  en América del Norte, América Central, la mayor parte de América del Sur y Japón.'),
(3, 'No Aplica', 'Juegos que no requieren de una TV');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `roles`
--

CREATE TABLE `roles` (
  `id_rol` int(11) NOT NULL,
  `nombre_rol` varchar(25) NOT NULL,
  `descripcion_rol` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `roles`
--

INSERT INTO `roles` (`id_rol`, `nombre_rol`, `descripcion_rol`) VALUES
(1, 'adm', 'Administrador - Administra el sistema. Privilegios Altos.'),
(2, 'usr', 'Usuario - Usuario estandar del sistema.'),
(3, 'NA', 'No Admitido - Usuario al que no se le permite acceder al sistema.');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL,
  `nombre_usu` varchar(50) NOT NULL,
  `ape_usu` varchar(50) NOT NULL,
  `correo` varchar(50) NOT NULL,
  `contra` varchar(250) NOT NULL,
  `avatar` varchar(40) NOT NULL,
  `estado` varchar(250) NOT NULL,
  `fecha_reg` date NOT NULL,
  `id_rol` int(11) NOT NULL,
  `telefono` varchar(12) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `nombre_usu`, `ape_usu`, `correo`, `contra`, `avatar`, `estado`, `fecha_reg`, `id_rol`, `telefono`) VALUES
(1, 'Admin', 'C. Gaming', 'adminCGaming@gmail.com', 'pbkdf2:sha256:260000$HEPH3dlg2wEZ5sqN$3948356cb0a90efc7ad5bf0f3228d6fa7c0df60e3067132e21e9abe75fd3a438', '2021-7-4-avatar-1.jpeg', 'México', '2021-07-04', 1, '5500000000');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `consolas`
--
ALTER TABLE `consolas`
  ADD PRIMARY KEY (`id_consola`);

--
-- Indices de la tabla `desarrolladoras`
--
ALTER TABLE `desarrolladoras`
  ADD PRIMARY KEY (`id_desarrolladora`);

--
-- Indices de la tabla `generos`
--
ALTER TABLE `generos`
  ADD PRIMARY KEY (`id_genero`);

--
-- Indices de la tabla `idiomas`
--
ALTER TABLE `idiomas`
  ADD PRIMARY KEY (`id_idioma`);

--
-- Indices de la tabla `juegos`
--
ALTER TABLE `juegos`
  ADD PRIMARY KEY (`id_juego`);

--
-- Indices de la tabla `regiones`
--
ALTER TABLE `regiones`
  ADD PRIMARY KEY (`id_region`);

--
-- Indices de la tabla `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id_rol`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `consolas`
--
ALTER TABLE `consolas`
  MODIFY `id_consola` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `desarrolladoras`
--
ALTER TABLE `desarrolladoras`
  MODIFY `id_desarrolladora` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `generos`
--
ALTER TABLE `generos`
  MODIFY `id_genero` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `idiomas`
--
ALTER TABLE `idiomas`
  MODIFY `id_idioma` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `juegos`
--
ALTER TABLE `juegos`
  MODIFY `id_juego` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `regiones`
--
ALTER TABLE `regiones`
  MODIFY `id_region` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `roles`
--
ALTER TABLE `roles`
  MODIFY `id_rol` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
